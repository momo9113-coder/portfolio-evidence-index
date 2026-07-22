"""Refresh a stable, compact inventory of every public owner repository."""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


API_ROOT = "https://api.github.com"
DEFAULT_OWNER = "momo9113-coder"
DEFAULT_OUTPUT = Path("generated/github-repositories.json")


def request_json(url: str, token: str | None = None) -> Any:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "portfolio-evidence-index",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(url, headers=headers)
    try:
        with urlopen(request, timeout=30) as response:
            return json.load(response)
    except HTTPError as exc:
        raise RuntimeError(f"GitHub API returned HTTP {exc.code} for {url}") from exc


def fetch_all_repositories(owner: str, token: str | None = None) -> list[dict[str, Any]]:
    repositories: list[dict[str, Any]] = []
    page = 1
    while True:
        query = urlencode(
            {
                "per_page": 100,
                "page": page,
                "type": "owner",
                "sort": "full_name",
                "direction": "asc",
            }
        )
        batch = request_json(f"{API_ROOT}/users/{owner}/repos?{query}", token)
        if not isinstance(batch, list):
            raise RuntimeError("GitHub repository response was not a list")
        repositories.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return repositories


def compact_repository(repository: dict[str, Any]) -> dict[str, Any]:
    full_name = repository["full_name"]
    branch = repository["default_branch"]
    return {
        "name": repository["name"],
        "full_name": full_name,
        "html_url": repository["html_url"],
        "api_url": repository["url"],
        "description": repository.get("description"),
        "is_fork": repository["fork"],
        "is_archived": repository["archived"],
        "visibility": repository["visibility"],
        "default_branch": branch,
        "created_at": repository["created_at"],
        "updated_at": repository["updated_at"],
        "pushed_at": repository["pushed_at"],
        "primary_language": repository.get("language"),
        "license_spdx": (repository.get("license") or {}).get("spdx_id"),
        "topics": repository.get("topics", []),
        "homepage": repository.get("homepage") or None,
        "readme_raw_url": f"https://raw.githubusercontent.com/{full_name}/{branch}/README.md",
        "contents_api_url": f"{API_ROOT}/repos/{full_name}/contents",
        "recursive_tree_api_url": f"{API_ROOT}/repos/{full_name}/git/trees/{branch}?recursive=1",
        "commits_api_url": f"{API_ROOT}/repos/{full_name}/commits?per_page=100",
        "releases_api_url": f"{API_ROOT}/repos/{full_name}/releases?per_page=100",
        "actions_api_url": f"{API_ROOT}/repos/{full_name}/actions/runs?per_page=20",
    }


def build_inventory(owner: str, token: str | None = None) -> dict[str, Any]:
    repositories = [
        compact_repository(repository)
        for repository in fetch_all_repositories(owner, token)
    ]
    repositories.sort(key=lambda item: item["full_name"].casefold())
    return {
        "schema_version": "1.0.0",
        "document_type": "github_public_repository_inventory",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "owner": owner,
        "source": f"{API_ROOT}/users/{owner}/repos",
        "repository_count": len(repositories),
        "interpretation_warning": "This includes forks. Repository visibility or ownership is not proof of original authorship; use portfolio.json for resume eligibility.",
        "repositories": repositories,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", default=DEFAULT_OWNER)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    token = os.environ.get("GITHUB_TOKEN") or None
    inventory = build_inventory(args.owner, token)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(inventory, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {inventory['repository_count']} repositories to {args.output}")


if __name__ == "__main__":
    main()
