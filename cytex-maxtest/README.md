# cytex-maxtest

A deliberate, self-contained test repository that exercises **every** scanner in
the Cytex security pipeline. Push it to a GitHub repo, let the platform scan it,
and confirm each source shows up in the consolidated report.

> ⚠️ Everything vulnerable or "malicious" here is a static test fixture pointed at
> `attacker-example.com` / `EXAMPLE` placeholders. Nothing runs and no value is a
> real secret. Do not reuse any of it in real code.

## What each file is for

| File | Scanner it triggers | Expected in report |
|------|--------------------|--------------------|
| `requirements.txt` | Syft SBOM, Grype/OSV CVEs, aibom dependency + model detectors | `components` (sbom + aibom), `vulnerabilities` (grype) |
| `package.json` | Syft SBOM, Grype/OSV CVEs (npm) | `components`, `vulnerabilities` |
| `ai_app.py` | aibom model / embedding / vector_store / prompt / memory / agent / tool detectors | `components` (`_source: aibom`) |
| `training.py` | aibom ml_lifecycle detector (training_run, model artifacts) | `components` |
| `vulnerable.py` | Semgrep SAST (eval, exec, command injection, SQLi, insecure deserialization, weak hash, TLS off) | `semgrep.results` |
| `config.py` | aibom secret_detector / detect-secrets / env_var_resolver | `components` (secret) |
| `.mcp.json` | aibom mcp_detector | `components` (mcp_server / mcp_client) |
| `Dockerfile` | aibom deployment_detector / container scanning | `components` |
| `data/customers.csv` | aibom data_file_scanner | `components` |
| `skills/summarizer/SKILL.md` | aibom skill_detector (inventory) + skill-scanner (benign) | `components` (type skill) |
| `skills/data-helper/**` | skill-scanner: prompt injection + data exfiltration + RCE | `vulnerabilities` (`_source: skills`) |
| `skills/system-cleanup/SKILL.md` | skill-scanner: pipeline taint (curl\|sh, exfil, miner) | `vulnerabilities` (`_source: skills`) |
| `mcp_server.py`, `mcp.json`, `.mcp.json` | aibom mcp_detector + mcp-scanner (tool poisoning) | `components` (mcp), `vulnerabilities` (`_source: mcp`) |
| `cloud.py` | aibom cloud detector (Bedrock, Vertex, Azure OpenAI) | `components` |
| `remote_agents.py`, `.well-known/agent.json` | aibom a2a / remote-agent detector | `components` |
| `shadow_ai.py` | aibom shadow_ai_detector (raw HTTP to LLM APIs) | `components` |
| `.github/workflows/ml-ci.yml` | aibom cicd_scanner (AI usage in CI) | `components` |
| `models/**` (`.safetensors`, `.gguf`, `.onnx`, `config.json`) | aibom model_file_scanner | `components` |
| `data/*.csv`, `data/train.jsonl` | aibom data_file_scanner | `components` |

Compliance verdicts (EU AI Act / OWASP-Agentic / NIST) land in `report.compliance`, the
flat inventory in `report.componentSummary`, and per-component enrichment (provider,
risk) is added by the agentic pass when the LLM model supports tool-calling.

## How to use

1. Create a **new empty** GitHub repo (e.g. `cytex-maxtest`).
2. Push the contents of this folder to it (see instructions from the assistant).
3. Register/scan that repo through the Cytex platform.
4. Open the consolidated report and check `cytexScan.summary` — you should see
   non-zero counts for components, vulnerabilities, sastFindings, skillComponents,
   and skillFindings.
