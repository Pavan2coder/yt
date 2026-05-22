# YouTube Assistant

An AI-powered Q&A assistant that watches YouTube videos for you. Paste a URL, ask a question, and get an answer based on the video's transcript — powered by **LangChain**, **Google Gemini**, and **FAISS** vector search, with a **Streamlit** frontend.

## How it works

1. Loads the transcript of any public YouTube video
2. Splits the transcript into searchable chunks
3. Embeds each chunk with Google's `gemini-embedding-001` model and stores them in a local FAISS vector index
4. When you ask a question, retrieves the most relevant transcript chunks
5. Feeds them to **Gemini 2.5 Flash** along with your question and returns a grounded answer

## Tech Stack

- **LLM:** Google Gemini 2.5 Flash
- **Embeddings:** Google `gemini-embedding-001`
- **Framework:** LangChain
- **Vector Store:** FAISS (local, in-memory)
- **UI:** Streamlit
- **Transcript Loader:** `youtube-transcript-api` via `YoutubeLoader`

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/Pavan2coder/yt.git
cd yt
```

### 2. Create a virtual environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your Google API key

Copy `.env.example` to `.env` and paste in your key:

```
Google_API_KEY="your-google-gemini-api-key-here"
```

Get a free key at https://aistudio.google.com/apikey.

### 5. Run the app

```bash
streamlit run main.py
```

The app opens at `http://localhost:8501`.

## Usage

1. Paste a YouTube video URL in the sidebar
2. Type your question
3. Click **Submit**
4. Read the answer (drawn only from facts in the transcript)

If the transcript doesn't contain enough information, the assistant will say **"I don't know"** rather than hallucinate.

## Project Structure

```
yt/
├── main.py                # Streamlit UI
├── langchain_helper.py    # LangChain pipeline (load -> embed -> retrieve -> answer)
├── requirements.txt       # Python dependencies
├── .env.example           # Template for environment variables
├── .gitignore
└── README.md
```

## Limitations

- Only works on YouTube videos that have transcripts/captions available
- FAISS index is built fresh on each query (no persistence between sessions)
- Answers are limited to what's actually said in the video

## License

MIT
