import os

from dotenv import load_dotenv

load_dotenv()

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore

def ingest_docs():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    loader = TextLoader("logs.txt", encoding="utf-8")
    raw_documents = loader.load()
    print(f"loaded {len(raw_documents)} documents")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)
    documents = text_splitter.split_documents(raw_documents)

    print(f"Going to add {len(documents)} documents to Pinecone")
    PineconeVectorStore.from_documents(
        documents, embeddings, index_name=os.environ["PINECONE_INDEX_NAME"]
    )
    print("*****Loading to vectorstore done*****")
if __name__ == "__main__":
    ingest_docs()
