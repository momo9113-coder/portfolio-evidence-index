# Portfolio Evidence Index

Machine-readable evidence for resume and application drafting. This repository is metadata, not a fourth portfolio project.

## Canonical entry points

- `portfolio.json`: routing and verification instructions for the three resume-eligible projects.
- `generated/github-repositories.json`: complete public GitHub inventory, including forks and non-portfolio repositories.
- `llms.txt`: short bootstrap instructions for an LLM or retrieval system.
- `portfolio.schema.json`: JSON Schema for the curated document.

The inventory is refreshed weekly from GitHub's public API. Project facts are intentionally not duplicated here; an LLM should inspect each source repository and evaluate its current evidence.

## Stable URLs

```text
https://raw.githubusercontent.com/momo9113-coder/portfolio-evidence-index/main/llms.txt
https://raw.githubusercontent.com/momo9113-coder/portfolio-evidence-index/main/portfolio.json
https://raw.githubusercontent.com/momo9113-coder/portfolio-evidence-index/main/generated/github-repositories.json
https://api.github.com/users/momo9113-coder/repos?per_page=100&type=owner&sort=updated
```

## Local verification

```bash
python scripts/refresh_github.py
python -m unittest discover -s tests -v
```

No token is required for local public-data refreshes. GitHub Actions may use its built-in short-lived `GITHUB_TOKEN`; this repository requires no custom secret.
