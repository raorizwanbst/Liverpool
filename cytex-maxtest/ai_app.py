"""
AI application surface for cisco-aibom detection.
Exercises: models, embeddings, vector stores, prompts, memory, agents/tools,
multiple providers (OpenAI, Anthropic, HuggingFace, Ollama). Nothing runs — this
is a static fixture; the strings and imports are what the detectors read.
"""
import os

import openai
from anthropic import Anthropic
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from langchain_chroma import Chroma
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import redis

# --- Models (model_detector) ---
openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
gpt4o = ChatOpenAI(model="gpt-4o")
gpt4o_mini = ChatOpenAI(model="gpt-4o-mini")
claude = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
CLAUDE_MODEL = "claude-sonnet-4-5"
local_llm = ChatOllama(model="llama3.1")
hf_generator = pipeline("text-generation", model="gpt2")

# --- Embeddings (embedding detector) ---
openai_embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
st_embeddings = SentenceTransformer("all-MiniLM-L6-v2")

# --- Vector store (vector_store detector) ---
vector_db = Chroma(embedding_function=openai_embeddings, collection_name="docs")

# --- Prompt (prompt detector) ---
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use the provided context."),
    ("human", "{question}"),
])

# --- Memory (memory detector) ---
memory = ConversationBufferMemory(memory_key="chat_history")
cache = redis.Redis(host="localhost", port=6379, db=0)


# --- Agent + tools (agent / tool detectors) ---
def _search(query: str) -> str:
    return f"results for {query}"


tools = [Tool(name="search", func=_search, description="Search the knowledge base")]
agent = create_react_agent(gpt4o, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, memory=memory)


def answer(question: str) -> str:
    docs = vector_db.similarity_search(question, k=4)
    return executor.invoke({"question": question, "context": docs})["output"]
