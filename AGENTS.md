# LLM Maintenance Contract

This repository is a public, machine-readable navigation index. It is not a portfolio project and must not be described as one. Do not duplicate project metrics or pre-write resume claims here; route the next LLM to source evidence and let it evaluate the current repositories.

## Before editing

1. Read `llms.txt`, `portfolio.json`, and the target project's immutable evidence links.
2. Refresh `generated/github-repositories.json` with `python scripts/refresh_github.py`.
3. Verify public commits, releases, CI, deployments, and time-sensitive competition results.

## Rules

- Include every public owner repository in the generated inventory, including forks.
- Include only evidence-backed authored work in `project_routes`.
- Keep routes, assessment questions, and interpretation boundaries concise.
- Require downstream LLMs to extract metrics from source repositories and pin final claims to immutable commits.
- Treat Kaggle scores and ranks as dated snapshots until final results are verified.
- Never copy private handoff files, local absolute paths, credentials, personal contact details, unpublished manuscript content, or raw restricted data here.
- Do not claim causality, production use, users, revenue, commercial impact, novelty, team size, awards, or publication status without direct evidence.

## Verification

```bash
python scripts/refresh_github.py
python -m unittest discover -s tests -v
```
