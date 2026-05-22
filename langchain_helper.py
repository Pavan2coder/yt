import os
from dotenv import load_dotenv

# --- Modern Document & Vector Store Imports ---
from langchain_community.document_loaders import YoutubeLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

# --- Modern Gemini AI Imports ---
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.prompts import PromptTemplate

# Load your GOOGLE_API_KEY from your .env file
load_dotenv()

# Set up the correct, active Gemini Embeddings model!
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

def create_db_from_youtube_video_url(video_url: str) -> FAISS:
    # 1. Load the YouTube transcript 
    loader = YoutubeLoader.from_youtube_url(video_url)
    transcript = loader.load()

    # 2. Chop text into searchable chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(transcript)

    # 3. Create local Vector Store index
    db = FAISS.from_documents(docs, embeddings)
    return db


def get_response_from_query(db, query, k=4):
    # 1. Pull the 4 most mathematically similar paragraph chunks
    docs = db.similarity_search(query, k=k)
    docs_page_content = " ".join([d.page_content for d in docs])

    # 2. Use Gemini 2.5 Flash as the processing brain
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

    # 3. Define prompt guidelines
    prompt = PromptTemplate(
        input_variables=["question", "docs"],
        template="""
        You are a helpful assistant that can answer questions about youtube videos 
        based on the video's transcript.
        
        Answer the following question: {question}
        By searching the following video transcript: {docs}
        
        Only use the factual information from the transcript to answer the question.
        
        If you feel like you don't have enough information to answer the question, say "I don't know".
        
        Your answers should be verbose and detailed.
        """,
    )

    # 4. Modern LangChain Chain syntax 
    chain = prompt | llm

    # 5. Invoke the chain and clean the string formatting
    response = chain.invoke({"question": query, "docs": docs_page_content})
    clean_response = response.content.replace("\n", "")
    
    return clean_response, docs