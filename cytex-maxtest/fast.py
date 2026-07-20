"""
Large FastAPI application for AIBOM testing.

Includes:
- FastAPI
- OpenAI SDK
- Anthropic SDK
- LangChain
- Hugging Face Transformers
- sentence-transformers
- Chroma Vector DB
- FAISS
- Ollama
- OpenAI Embeddings
- Hugging Face embeddings
- Torch
- NumPy
- Pandas
"""

import os
import numpy as np
import pandas as pd
import torch

from fastapi import FastAPI
from pydantic import BaseModel

from openai import OpenAI
from anthropic import Anthropic

from sentence_transformers import SentenceTransformer

from transformers import (
    pipeline,
    AutoTokenizer,
    AutoModelForSequenceClassification,
    AutoModelForCausalLM,
)

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama

import faiss


app = FastAPI(title="AIBOM Demo API")


###########################################################################
# Global Models
###########################################################################

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

anthropic_client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

sentence_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

tokenizer = AutoTokenizer.from_pretrained(
    "distilbert-base-uncased-finetuned-sst-2-english"
)

classifier_model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased-finetuned-sst-2-english"
)

classifier = pipeline(
    "sentiment-analysis",
    model=classifier_model,
    tokenizer=tokenizer,
)

generator = pipeline(
    "text-generation",
    model="gpt2",
)

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vector_store = Chroma(
    collection_name="documents",
    embedding_function=embeddings,
)

ollama = ChatOllama(
    model="llama3.1"
)

langchain_llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Answer briefly."
        ),
        (
            "user",
            "{question}"
        ),
    ]
)

chain = prompt | langchain_llm

faiss_index = faiss.IndexFlatL2(384)

###########################################################################
# Request Models
###########################################################################

class PromptRequest(BaseModel):
    prompt: str


class TextRequest(BaseModel):
    text: str


class EmbeddingRequest(BaseModel):
    sentences: list[str]


###########################################################################
# Routes
###########################################################################

@app.get("/")
def root():
    return {
        "message": "AIBOM Test Application",
        "torch": torch.__version__,
        "numpy": np.__version__,
        "pandas": pd.__version__,
    }


@app.post("/openai")
def openai_chat(req: PromptRequest):
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": req.prompt,
            }
        ],
    )

    return {
        "response": response.choices[0].message.content
    }


@app.post("/anthropic")
def anthropic_chat(req: PromptRequest):
    response = anthropic_client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        messages=[
            {
                "role": "user",
                "content": req.prompt,
            }
        ],
    )

    return {
        "response": response.content[0].text
    }


@app.post("/langchain")
def langchain_chat(req: PromptRequest):
    result = chain.invoke(
        {
            "question": req.prompt
        }
    )

    return {
        "response": result.content
    }


@app.post("/ollama")
def ollama_chat(req: PromptRequest):
    response = ollama.invoke(req.prompt)

    return {
        "response": response.content
    }


@app.post("/sentiment")
def sentiment(req: TextRequest):
    return classifier(req.text)


@app.post("/generate")
def generate(req: PromptRequest):
    return generator(
        req.prompt,
        max_new_tokens=40,
    )


@app.post("/embed")
def embed(req: EmbeddingRequest):
    vectors = sentence_model.encode(
        req.sentences
    )

    return {
        "dimension": len(vectors[0]),
        "count": len(vectors),
    }


@app.post("/openai-embeddings")
def openai_embeddings(req: EmbeddingRequest):
    vectors = embeddings.embed_documents(
        req.sentences
    )

    return {
        "count": len(vectors)
    }


@app.post("/vector-store")
def add_documents(req: EmbeddingRequest):
    vector_store.add_texts(req.sentences)

    return {
        "stored": len(req.sentences)
    }


@app.post("/vector-search")
def search(req: PromptRequest):
    docs = vector_store.similarity_search(
        req.prompt,
        k=3,
    )

    return {
        "results": [d.page_content for d in docs]
    }


@app.post("/faiss")
def add_to_faiss(req: EmbeddingRequest):
    vectors = sentence_model.encode(
        req.sentences
    ).astype("float32")

    faiss_index.add(vectors)

    return {
        "total_vectors": faiss_index.ntotal
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "services": [
            "OpenAI",
            "Anthropic",
            "LangChain",
            "Ollama",
            "Transformers",
            "SentenceTransformers",
            "Chroma",
            "FAISS",
            "Torch",
        ],
    }
