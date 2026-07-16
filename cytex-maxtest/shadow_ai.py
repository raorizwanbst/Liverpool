"""
Shadow AI surface for cisco-aibom's shadow_ai_detector.

Shadow AI = an AI package IMPORTED in code but NOT declared in requirements.txt.
Every package imported below is deliberately ABSENT from requirements.txt. This is a
broad batch of canonical, widely-known AI packages so that whichever ones cisco-aibom's
knowledge base recognizes get flagged as undeclared ("shadow_ai": true). Static fixture
— imports do not resolve at runtime, which is fine; the detector reads the import lines.
"""
import importlib

# Google / HuggingFace ecosystem
import google.generativeai as genai
import huggingface_hub
import accelerate
import datasets
import diffusers
import peft
import tiktoken

# Providers / frameworks
import cohere
import pinecone
import llama_index
import autogen
import litellm
import langgraph
import crewai
import instructor
import vllm

# Dynamic imports (also matched by the detector's import-call patterns)
haystack = importlib.import_module("haystack")
sk = __import__("semantic_kernel")


def gemini(prompt):
    genai.configure(api_key="unused")
    return genai.GenerativeModel("gemini-1.5-pro").generate_content(prompt)


def rerank(query, docs):
    return cohere.Client("unused").rerank(query=query, documents=docs, model="rerank-english-v3.0")


def upsert(vectors):
    return pinecone.Pinecone(api_key="unused").Index("shadow").upsert(vectors)
