"""
Config surface for secret_detector / detect-secrets / env_var_resolver.
All values below are FAKE placeholders (EXAMPLE / documented dummy values) — they
are here to trip secret detection, not to be used. Do not put real secrets here.
"""
import os

# Resolved from the environment (env_var_resolver picks these up)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Hardcoded fakes (secret_detector / semgrep keyword rules)
DATABASE_PASSWORD = "P@ssw0rd-EXAMPLE-not-real"
JWT_SIGNING_SECRET = "this_is_a_fake_signing_secret_EXAMPLE_1234567890"

# AWS documented example credentials (safe, well-known dummy values)
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# Fake provider tokens (obviously not real)
OPENAI_KEY_HARDCODED = "sk-proj-FAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKEEXAMPLE"
SLACK_WEBHOOK = "https://hooks.slack.com/services/T00000000/B00000000/EXAMPLEEXAMPLE"
