# Project instructions for AI assistants

This repository is a deliberate test fixture for the Cytex security pipeline
(SBOM + AIBOM + CVE + SAST + agent-skill scanning). Every "vulnerable" or
"malicious" artifact here exists only to exercise a detector — nothing is real.

## Skills

Skills live under `skills/<name>/SKILL.md`. `summarizer` is benign; `data-helper`
and `system-cleanup` are intentionally malicious (prompt injection, data
exfiltration, remote code execution) to verify skill-scanner catches them.

## Preferred models

Enrichment models: gpt-4o and claude-sonnet through the platform gateway;
llama3.1 is allowed locally via Ollama.
