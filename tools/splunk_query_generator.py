from langchain.tools import tool
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
import os

@tool
def generate_splunk_query(user_question: str) -> str:
    """Converts user question into a Splunk expression using log structure and semantic examples."""

    # Load from vector store
    embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = PineconeVectorStore(index_name=os.environ["PINECONE_INDEX_NAME"], embedding=embedding_model)
    retriever = vectorstore.as_retriever(search_type="similarity", k=4)
    context_docs = retriever.invoke(user_question)
    context_text = "\n".join([doc.page_content for doc in context_docs])

    # Schema explanation
    schema_description = """
The logs are structured key-value pairs per line like:
index=abc APPLICATION=<microservice> ACTION=<action> ... EVENT_ID=<UUID>

Field meanings:
- APPLICATION: Name of the microservice generating the log.
- ACTION: Type of event (e.g., INPUT_EVENT, OUTPUT_EVENT, EVENT_PROCESSED).
- EVENT_ID: UUID for tracing a specific message or event through the system.
- Other fields may include SYMBOL (stock symbol), PRICE, QTY, USER_ID, etc.

Understanding:
- If user asks about "why a stock wasn't processed", ACTION like EVENT_PROCESSED or FAILURE must be queried.
- For tracing, use EVENT_ID across multiple APPLICATIONs.
- For data from specific services, filter using APPLICATION=<service_name>.
- Time range should be inferred from user's query context if possible.
"""

    # New Prompt Template
    prompt = PromptTemplate.from_template(
        """You are an expert in Splunk and log analysis.

{schema}

Use the following example logs to understand the structure and format:
--------------------
{context}
--------------------

Now, based on the user's query:
"{question}"

Generate the appropriate Splunk query (SPL). Only return the SPL query expression."""
    )

    llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.2)
    chain = LLMChain(llm=llm, prompt=prompt)

    response = chain.invoke({
        "schema": schema_description.strip(),
        "context": context_text.strip(),
        "question": user_question.strip()
    })

    return response["text"]
