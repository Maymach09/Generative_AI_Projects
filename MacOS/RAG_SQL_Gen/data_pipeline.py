from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma
import os
import shutil
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

CHROMA_PATH = "/Users/maymach09/Documents/GenAI09/MacOS/RAG_SQL_Gen/chromaDB"
DATA_PATH = "/Users/maymach09/Documents/GenAI09/MacOS/RAG_SQL_Gen/data"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        generate_data_store()
        logger.info("Data pipeline execution completed successfully.")
    except Exception as e:
        logger.error(f"Error occurred during data pipeline execution: {e}")


def generate_data_store():
    documents = load_documents()
    print("Document:", len(documents))
    chunks = split_text(documents)
    save_to_chroma(chunks)


# def load_documents():
#     loader = PyPDFDirectoryLoader(DATA_PATH)
#     documents = loader.load()
#     return documents

def load_documents():
    try:
        if not os.path.exists(DATA_PATH):
            raise FileNotFoundError(f"File not found at path: {DATA_PATH}")

        loader = PyPDFDirectoryLoader(DATA_PATH)
        documents = loader.load()
        logger.info(f"Loaded {len(documents)} documents from {DATA_PATH}.")
        return documents
    except Exception as e:
        logger.error(f"Error occurred while loading documents: {e}")
        return []

def split_text(documents: list[Document]):
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=100,
            length_function=len,
            add_start_index=True,
        )
        chunks = text_splitter.split_documents(documents)
        logger.info(f"Split {len(documents)} documents into {len(chunks)} chunks.")
        return chunks
    except Exception as e:
        logger.error(f"Error occurred while splitting text: {e}")
        return []

def save_to_chroma(chunks: list[Document]):
    try:
        # Clear out the database first.
        if os.path.exists(CHROMA_PATH):
            shutil.rmtree(CHROMA_PATH)

        # Create a new DB from the documents.
        openai_api_key = os.environ.get('OPENAI_API_KEY')
        print(openai_api_key)
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        db = Chroma.from_documents(
            documents=chunks, embedding=embeddings, persist_directory=CHROMA_PATH
        )
        db.persist()
        logger.info(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")
    except Exception as e:
        logger.error(f"Error occurred while saving chunks to Chroma DB: {e}")



if __name__ == "__main__":
    main()