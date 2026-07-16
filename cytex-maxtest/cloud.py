"""
Cloud AI surface for cisco-aibom's cloud resource scanner: AWS Bedrock, Google
Vertex AI, and Azure OpenAI. Static fixture — nothing connects at runtime.
"""
import os

import boto3
import vertexai
from vertexai.generative_models import GenerativeModel
from openai import AzureOpenAI

# --- AWS Bedrock (cloud: aws) ---
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")
BEDROCK_MODEL = "anthropic.claude-3-5-sonnet-20240620-v1:0"
bedrock_titan = "amazon.titan-embed-text-v2:0"

# --- Google Vertex AI (cloud: gcp) ---
vertexai.init(project="cytex-maxtest", location="us-central1")
gemini = GenerativeModel("gemini-1.5-pro")

# --- Azure OpenAI (cloud: azure) ---
azure_client = AzureOpenAI(
    azure_endpoint="https://cytex-maxtest.openai.azure.com/",
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01",
)
AZURE_DEPLOYMENT = "gpt-4o-cytex"


def bedrock_infer(prompt: str):
    return bedrock.invoke_model(modelId=BEDROCK_MODEL, body=prompt)


def vertex_infer(prompt: str):
    return gemini.generate_content(prompt)


def azure_infer(prompt: str):
    return azure_client.chat.completions.create(
        model=AZURE_DEPLOYMENT, messages=[{"role": "user", "content": prompt}]
    )
