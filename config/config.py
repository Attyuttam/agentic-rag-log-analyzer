from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0)
embedding_llm=GoogleGenerativeAIEmbeddings(model="models/embedding-001")
log_index="trading_logs"