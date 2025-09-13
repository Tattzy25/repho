"""
AI Gateway Model Lineup for Orchestrator & Agents
"""
MODELS = {
    "orchestrator": "openai/gpt-4o",
    "helix": "openai/gpt-oss-120b",
    "echo": "openai/gpt-oss-120b",
    "forge": "xai/grok-code-fast-1",
    "scout": "xai/grok-code-fast-1",
    "embeddings": "openai/text-embedding-3-large",
    "embeddings_alt": "mistral/mistral-embed",
    "vision": "openai/dalle-3",
    "code": "mistral/codestral",
    "sonnet": "anthropic/claude-sonnet-4"
}

# Usage example:
# model = MODELS["orchestrator"]
