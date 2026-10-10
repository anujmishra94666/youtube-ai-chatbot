
import streamlit as st

import re

from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS

from langchain_groq import ChatGroq

from langchain_core.prompts import ChatPromptTemplate

from langchain_core.output_parsers import StrOutputParser


# --------------------------------------------------
# Step 1 — Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="YouTube AI Chatbot",
    page_icon="▶️",
    layout="wide"
)

st.title("▶️ YouTube AI Chatbot")

st.write(
    "Welcome! Ask questions about any YouTube video."
)


# --------------------------------------------------
# step 2 : UI Styling
# --------------------------------------------------

st.markdown("""
<style>

/* Main page background */
.stApp {
    background-color: #0b1120;
    color: #f1f5f9;
}

/* Sidebar background */
[data-testid="stSidebar"] {
    background-color: #111827;
}

/* Main heading */
h1 {
    color: #60a5fa;
    font-size: 40px !important;
}

/* Normal text */
p {
    color: #cbd5e1;
    font-size: 17px;
}

/* Buttons */
.stButton > button {
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 20px;
}

/* Button hover effect */
.stButton > button:hover {
    background-color: #1d4ed8;
    color: white;
    border: 1px solid #60a5fa;
}

/* Chat input */
[data-testid="stChatInput"] {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# Step 3 — Session State
# --------------------------------------------------

# Streamlit rerun hone par bhi vector store aur chat history save rahegi

if "vector_store" not in st.session_state:
    st.session_state["vector_store"] = None

if "video_id" not in st.session_state:
    st.session_state["video_id"] = None

if "messages" not in st.session_state:
    st.session_state["messages"] = []


# --------------------------------------------------
# step - 4 function for trim the id from the url of the youtube video
# --------------------------------------------------

def extract_video_id(url):

    url = url.strip()

    # Agar user sirf video ID dale
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", url):
        return url

    # YouTube URL se ID nikaalna
    patterns = [
        r"(?:youtube\.com/watch\?v=)([A-Za-z0-9_-]{11})",
        r"(?:youtu\.be/)([A-Za-z0-9_-]{11})",
        r"(?:youtube\.com/embed/)([A-Za-z0-9_-]{11})",
        r"(?:youtube\.com/shorts/)([A-Za-z0-9_-]{11})"
    ]

    for pattern in patterns:

        match = re.search(pattern, url)

        if match:
            return match.group(1)

    return None


# --------------------------------------------------
# step - 5
# --------------------------------------------------

def fetch_transcript(video_id):

    ytt_api = YouTubeTranscriptApi()

    transcript = ytt_api.fetch(
        video_id,
        languages=["hi", "en"]
    )

    transcript_list = transcript.to_raw_data()

    transcript_text = " ".join(
        chunk["text"] for chunk in transcript_list
    )

    return transcript_text


# --------------------------------------------------
# Step 3 — Sidebar aur YouTube Video Input banate hain.
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.title("▶️ YouTube AI")

    st.write("Your personal video assistant")

    st.divider()

    st.subheader("🎬 Video Settings")

    video_url = st.text_input(
        "YouTube Video URL",
        placeholder="Paste your YouTube link here"
    )

    load_video = st.button(
        "📥 Load Video",
        use_container_width=True
    )

    st.divider()

    st.subheader("💡 Try asking")

    st.write("📝 Summarize this video")

    st.write("🎯 What are the main points?")

    st.write("🔍 Explain a topic")


# --------------------------------------------------
# Step 6 — Transcript ko chunks mein split karna
# Step 7 — Embeddings + FAISS Vector Store
# --------------------------------------------------

# Chunks = Transcript ke text pieces

# HuggingFace Embeddings = Text ko numerical vectors mein convert karta hai

# FAISS Vector Store = Vectors ko store karke relevant text search karta hai


if load_video:

    video_id = extract_video_id(video_url)

    if video_id:

        try:

            # Step 5: Pehle transcript fetch hoga

            with st.spinner("Fetching video transcript..."):

                transcript_text = fetch_transcript(video_id)

            if not transcript_text.strip():
                st.error("Transcript empty hai.")
                st.stop()

            st.session_state["transcript"] = transcript_text

            st.session_state["video_id"] = video_id

            st.success("Transcript loaded successfully!")

            st.write(
                "Transcript length:",
                len(transcript_text),
                "characters"
            )

            # Step 6: Transcript ko chunks mein split karna

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )

            chunks = splitter.create_documents(
                [transcript_text]
            )

            st.success("Transcript split successfully!")

            st.write("Total chunks:", len(chunks))

            # Step 7: Embeddings + FAISS Vector Store

            with st.spinner("Creating embeddings and vector store..."):

                embeddings = HuggingFaceEmbeddings(
                    model_name="sentence-transformers/all-MiniLM-L6-v2"
                )

                vector_store = FAISS.from_documents(
                    chunks,
                    embeddings
                )

            st.session_state["vector_store"] = vector_store

            # Naya video load hone par purani chat clear karna
            st.session_state["messages"] = []

            st.success("Video is ready for questions!")

        except TranscriptsDisabled:

            st.error("Is video ke captions available nahi hain.")

        except Exception as e:

            st.error(f"Error: {e}")

    else:

        st.error("Invalid YouTube URL or Video ID!")


# --------------------------------------------------
# Step 8 — Retriever banana
# --------------------------------------------------

# Retriever question ke according relevant chunks search karega


# --------------------------------------------------
# Step 9 — Prompt aur Groq LLM
# --------------------------------------------------

prompt = ChatPromptTemplate.from_template("""
You are a helpful YouTube video assistant.

Answer the question using only the provided video context.
If the answer is not available in the context, say that
the information was not found in the video transcript.

Context:
{context}

Question:
{question}

Answer:
""")

# Groq LLM use kar rahe hain

# API key .streamlit/secrets.toml file mein rakho
# GROQ_API_KEY = "your_actual_groq_api_key"

try:

    groq_api_key = st.secrets["GROQ_API_KEY"]

    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0,
        api_key=groq_api_key
    )

    # Prompt -> LLM -> Output Parser
    answer_chain = prompt | llm | StrOutputParser()

except Exception:

    answer_chain = None


# --------------------------------------------------
# Step 10 — Chat History Display
# --------------------------------------------------

for message in st.session_state["messages"]:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# --------------------------------------------------
# Step 11 — User ka question aur final answer
# --------------------------------------------------

question = st.chat_input(
    "Ask something about the video..."
)

if question:

    if st.session_state["vector_store"] is None:

        st.warning("Please load a YouTube video first.")

    elif answer_chain is None:

        st.error(
            "Groq API key nahi mili. "
            "Please .streamlit/secrets.toml configure karo."
        )

    else:

        # User ka question chat history mein add karna

        st.session_state["messages"].append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):

            st.markdown(question)

        try:

            with st.chat_message("assistant"):

                with st.spinner("Searching video and generating answer..."):

                    # Step 8 — Retriever banana
                    retriever = st.session_state[
                        "vector_store"
                    ].as_retriever(
                        search_kwargs={"k": 4}
                    )

                    # Relevant chunks retrieve karna
                    retrieved_docs = retriever.invoke(question)

                    # Retrieved chunks ko context mein convert karna
                    context = "\n\n".join(
                        doc.page_content
                        for doc in retrieved_docs
                    )

                    # Step 9 — Groq se answer generate karna
                    answer = answer_chain.invoke({
                        "context": context,
                        "question": question
                    })

                st.markdown(answer)

            # Assistant ka answer history mein save karna
            st.session_state["messages"].append({
                "role": "assistant",
                "content": answer
            })

        except Exception as e:

            st.error(f"Answer generate nahi hua: {e}")




            # https://github.com/anujmishra94666/youtube-ai-chatbot.git