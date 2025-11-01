from core.config import get_llm
import chromadb
from sentence_transformers import SentenceTransformer
import numpy as np
from langchain_text_splitters import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader


pdf_path = "C:\\Users\\Arun\\Documents\\scalable_agent_system\\graph\\nodes\\Blaupunkt_Manual.pdf"
pdf_reader = PdfReader(pdf_path)
llm = get_llm()
# Extract text
raw_text = ""
for page in pdf_reader.pages:
    raw_text += page.extract_text() + "\n"

# Split into manageable chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,   # adjust size based on your use case
    chunk_overlap=50
)
chunks = splitter.split_text(raw_text)
# Initialize Chroma client
chroma_client = chromadb.PersistentClient(path="chroma_db")
# Create or get collection
collection = chroma_client.get_or_create_collection("blaupunkt_pdf")
# Load embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")
# Generate embeddings
embeddings = embedder.encode(chunks).tolist()

# Add to Chroma
collection.add(
    documents=chunks,
    embeddings=embeddings,
    ids=[f"doc_{i}" for i in range(len(chunks))]
)
# 4. Retrieval function
def vector_retrieve(query, top_k=3):
    """
    Retrieve the most relevant documents from the vector database for a given query.

    This function encodes the input query into an embedding vector using the
    predefined `embedder` model and performs a similarity search against the
    existing document embeddings in the `collection`. It returns the top `k`
    most relevant documents based on vector similarity.

    Args:
        query (str): The user query or search phrase.
        top_k (int, optional): The number of top-matching documents to return.
            Defaults to 3.

    Returns:
        list[str]: A list of the top-matching document contents corresponding
        to the given query.
    """
    query_embedding = embedder.encode([query]).tolist()[0]
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results["documents"][0]

def rag_query_handler(query):
    """
    Handles retrieval-augmented generation (RAG) queries by fetching relevant context
    from a vector database and generating a response using a language model.

    The function first retrieves semantically similar document chunks related to the
    user's query using vector similarity search. If relevant context is found, it builds
    a natural language prompt containing the retrieved context and the user’s query.
    This prompt is then passed to the Mistral model (via OpenRouter API) to generate
    a context-based response. If no context is found or an error occurs, an appropriate
    fallback message is returned.

    Args:
        query (str): The user query or information request.

    Returns:
        str: The generated response based on the retrieved context, or an error or
        fallback message if no context is available.
    """
    # 1️⃣ Retrieve relevant context
    relevant_contexts = vector_retrieve(query, top_k=3)
    relevant_context = "\n\n".join(relevant_contexts)

    if not relevant_context:
        return (
            "I'm sorry, I couldn't find any relevant information in my documents about that."
        )

    # 2️⃣ Build router-style prompt
    router_prompt = f"""You are a helpful sales executive. Based ONLY on the provided context, answer the user's question.
If the answer is not in the context, say that you cannot find the information in the provided documents.

Context:
{relevant_context}

User Query: {query}
'''"""

    # 3️⃣ Generate response using OpenRouter API (Mistral model)
    try:
        response = llm.chat.completions.create(
            model="mistralai/mistral-7b-instruct-v0.2",
            messages=[{"role": "user", "content": router_prompt}],
        )

        raw_output = response.choices[0].message.content.strip()
        return raw_output

    except Exception as e:
        return f"⚠️ An error occurred while generating a response: {e}"