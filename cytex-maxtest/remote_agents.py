"""
Remote / agent-to-agent (A2A) surface for cisco-aibom's a2a_detector and remote
agent resolution. References the A2A protocol, an agent card, and remote agent
endpoints. Static fixture.
"""
import httpx
from a2a.client import A2AClient
from a2a.types import AgentCard

# Remote agent endpoints (A2A / remote agent resolution)
REMOTE_AGENTS = {
    "billing-agent": "https://agents.example.com/billing/.well-known/agent.json",
    "support-agent": "https://agents.example.com/support/.well-known/agent.json",
}

card = AgentCard(
    name="cytex-orchestrator",
    description="Routes tasks to remote specialist agents over A2A.",
    url="https://agents.example.com/orchestrator",
    version="1.0.0",
)


def call_remote_agent(name: str, task: str):
    client = A2AClient(url=REMOTE_AGENTS[name])
    return client.send_task({"message": task})


def discover(url: str):
    # fetch a remote agent card (.well-known/agent.json)
    return httpx.get(url + "/.well-known/agent.json").json()
