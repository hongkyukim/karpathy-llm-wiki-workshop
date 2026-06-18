#!/usr/bin/env python3
import argparse
import base64
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

API = "https://api.github.com"


def request_json(url: str, token: str | None = None):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "llm-wiki-workshop"})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def slug(owner: str, repo: str) -> str:
    return f"{owner}--{repo}".lower().replace("_", "-")


def write_raw(path: Path, source_url: str, body: str) -> None:
    digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
    fm = f"---\nsource_url: {source_url}\ningested: {date.today().isoformat()}\nsha256: {digest}\n---\n"
    path.write_text(fm + body, encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repos", default="data/repos.json")
    ap.add_argument("--vault", default="vault")
    args = ap.parse_args()
    repos = json.loads(Path(args.repos).read_text(encoding="utf-8"))
    out = Path(args.vault) / "raw" / "github"
    out.mkdir(parents=True, exist_ok=True)
    token = os.environ.get("GITHUB_TOKEN")
    failures = []
    for item in repos:
        owner, repo = item["owner"], item["repo"]
        name = slug(owner, repo)
        try:
            meta = request_json(f"{API}/repos/{owner}/{repo}", token)
            try:
                readme_resp = request_json(f"{API}/repos/{owner}/{repo}/readme", token)
                readme = base64.b64decode(readme_resp.get("content", "")).decode("utf-8", "replace")
            except Exception as exc:
                readme = f"README fetch failed: {exc}\n"
            record = {
                "source": "github",
                "url": f"https://github.com/{owner}/{repo}",
                "owner": owner,
                "repo": repo,
                "focus": item.get("focus", ""),
                "description": meta.get("description"),
                "homepage": meta.get("homepage"),
                "stars": meta.get("stargazers_count"),
                "forks": meta.get("forks_count"),
                "language": meta.get("language"),
                "topics": meta.get("topics", []),
                "license": (meta.get("license") or {}).get("spdx_id"),
                "pushed_at": meta.get("pushed_at"),
                "created_at": meta.get("created_at"),
                "readme_excerpt": readme[:12000],
            }
            body = json.dumps(record, indent=2, sort_keys=True)
            write_raw(out / f"{name}.json", record["url"], body)
            write_raw(out / f"{name}-readme.md", record["url"] + "#readme", readme)
            print(f"captured {owner}/{repo}")
        except urllib.error.HTTPError as exc:
            failures.append(f"{owner}/{repo}: HTTP {exc.code} {exc.reason}")
        except Exception as exc:
            failures.append(f"{owner}/{repo}: {type(exc).__name__}: {exc}")
    if failures:
        print("Failures:", file=sys.stderr)
        for f in failures:
            print(f"- {f}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
