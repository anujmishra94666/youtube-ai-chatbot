# ▶️ YouTube AI Chatbot

**Chat with any YouTube video using AI!** 🚀

An AI-powered chatbot that understands YouTube video transcripts and answers user questions using Retrieval-Augmented Generation (RAG). Instead of watching an entire video, users can ask questions and get answers based on its transcript.

## 🌐 Live Demo

🔗 **Try the App:** (https://youtube-ai-chatbot-ghjqgusdrl2tmkzorq6hha.streamlit.app/)

## ✨ Features

- 🎬 **YouTube Video Integration** — Load videos using a YouTube URL or video ID.
- 📝 **Transcript Extraction** — Fetches available Hindi and English transcripts.
- ✂️ **Text Chunking** — Splits transcripts into smaller, manageable chunks.
- 🧠 **Semantic Search** — Uses Hugging Face embeddings to represent text as vectors.
- 🔍 **Context Retrieval** — FAISS retrieves relevant transcript chunks based on the user's question.
- 🤖 **AI-Powered Answers** — Uses Groq LLMs to generate context-based responses.
- 💬 **Interactive Chat Interface** — Ask multiple questions through a Streamlit chat UI.
- 🎨 **Custom UI** — Dark-themed interface with a sidebar for video settings.
- 🔐 **Secure API Configuration** — Keeps the Groq API key in Streamlit secrets.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web interface |
| LangChain | LLM and RAG workflow |
| Groq | LLM inference |
| Hugging Face | Text embeddings |
| Sentence Transformers | Text vectorization model |
| FAISS | Vector storage and similarity search |
| YouTube Transcript API | Transcript extraction |

## ⚙️ How It Works

1. **Enter a YouTube URL:** Paste a video link into the sidebar.
2. **Extract the Transcript:** The application fetches available captions.
3. **Split the Text:** The transcript is divided into overlapping chunks.
4. **Generate Embeddings:** Hugging Face converts chunks into numerical vectors.
5. **Store and Retrieve:** FAISS searches for the most relevant chunks.
6. **Generate an Answer:** The retrieved context and user question are sent to the Groq-powered LLM.
7. **Display the Response:** The answer appears in the chat interface.

## 🏗️ Architecture

```text
YouTube Video URL
       |
       v
Extract Video ID
       |
       v
Fetch Transcript
       |
       v
Text Splitting
       |
       v
Hugging Face Embeddings
       |
       v
FAISS Vector Store
       |
       v
User Question
       |
       v
Retriever (Top 4 Chunks)
       |
       v
Context + Question
       |
       v
Groq LLM + LangChain
       |
       v
AI-Generated Answer
```

## 💻 Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/youtube-ai-chatbot.git
```

### 2. Navigate to the Project Directory

```bash
cd youtube-ai-chatbot
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the Groq API Key

Create a file named `secrets.toml` inside the `.streamlit` folder.

Your project structure should look like this:

```text
youtube-ai-chatbot/
├── app.py
├── requirements.txt
├── .gitignore
└── .streamlit/
    └── secrets.toml
```

Add your Groq API key to `.streamlit/secrets.toml`:

```toml
GROQ_API_KEY = "your_actual_groq_api_key"
```

Get an API key from the [Groq Console](https://console.groq.com/keys).

### 6. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

## 🔐 Security

- Never upload API keys or `.streamlit/secrets.toml` to GitHub.
- Configure secrets through Streamlit Community Cloud when deploying.
- Keep your API credentials private.

## ⚠️ Limitations

- The video must have an accessible transcript.
- Videos without available captions may not work.
- Answers depend on the information present in the retrieved transcript chunks.
- The application requires an internet connection and a working Groq API key.
- Response speed and availability may depend on hosting resources and API limits.

## 🚀 Deployment

This application is deployed using **Streamlit Community Cloud**.

To deploy your own version:

1. Fork or clone this repository.
2. Push your code to GitHub.
3. Connect your repository to [Streamlit Community Cloud](https://share.streamlit.io/).
4. Set `app.py` as the main file.
5. Configure `GROQ_API_KEY` in the app's Secrets settings.
6. Deploy and start chatting with YouTube videos.

## 📚 Key Concepts Learned

- Retrieval-Augmented Generation (RAG)
- Text splitting and chunk overlap
- Embeddings and vector similarity search
- Vector stores and retrievers
- LangChain prompt templates and output parsers
- LLM integration using Groq
- Streamlit session state and chat interfaces
- Deploying Python AI applications

## 🔮 Future Improvements

- Support for video summaries and key takeaways
- Display relevant transcript excerpts with timestamps
- Add multilingual question answering
- Improve retrieval quality with advanced RAG techniques
- Add conversation memory
- Support playlists and multiple video sources

## 👨‍💻 Author

**Anuj Mishra**

Aspiring AI Engineer | Python | Generative AI | LangChain | RAG

- GitHub: (https://github.com/anujmishra94666)
- LinkedIn: (www.linkedin.com/in/anuj-mishr-0136b41b6)

---

⭐ If you find this project useful, consider giving it a star!

**Built with Python, LangChain, Groq, Hugging Face, FAISS and Streamlit.**
