# Operational Rules

- No fallbacks except those inherent to AI Gateway; all other errors must surface immediately.
- No authentication; the system runs locally for a single user.
- Agents have distinct futuristic names and singular goals; **Atlas**, **Spectra**, **Forge**, and **Sentinel** focus only on their assigned phase while **Nexus** replaces any agent that drifts.
- Execute tasks sequentially to avoid overlap; orchestrator governs timing.
- Log every action and stream updates in real time to the six-interface dashboard.
- Provide emergency stop and pause controls.
- Maintain modular naming: paths clearly marked as `backend` or `frontend`.
- Use only modern components and technologies from Vercel AI SDK and shadcn UI.
- All configurations rely on a single API key or OIDC for AI Gateway; model choices require approval.
