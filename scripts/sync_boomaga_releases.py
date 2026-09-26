#!/usr/bin/env python3

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib import error, request


GITHUB_API = "https://api.github.com/repos/{repo}/releases/latest"


def fetch_latest_release(repo: str):
    url = GITHUB_API.format(repo=repo)
    req = request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "Boomaga-site-sync",
        },
    )
    try:
        with request.urlopen(req) as response:
            return json.load(response)
    except error.HTTPError as exc:
        raise RuntimeError(f"GitHub API request failed: {exc.code} {exc.reason}") from exc


def release_version(tag: str) -> str:
    return tag[1:] if tag.startswith("v") else tag


def render_post(tag: str, published_at: str, body: str) -> str:
    version = release_version(tag)
    clean_body = (body or "").strip()
    if clean_body:
        body_block = f"\n{clean_body}\n"
    else:
        body_block = ""

    release_date = published_at[:10] if published_at else date.today().isoformat()
    return (
        "---\n"
        "categories : [releases]\n"
        "---\n\n"
        f"Boomaga {version} is out!\n"
        "=====================\n"
        "We are glad to announce a new version of Boomaga.\n"
        f"{body_block}\n"
        "See the release notes and changelog here:\n"
        f"* https://github.com/Boomaga/boomaga/releases/tag/{tag}\n"
    )


def update_config_version(config_path: str, tag: str, dry_run: bool = False) -> str:
    version = release_version(tag)
    config_file = Path(config_path)
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_file}")

    original = config_file.read_text(encoding="utf-8")
    pattern = r"(?ms)(^program:\n\s*release:\n\s*version:\s*)([^\n]+)"
    updated = re.sub(pattern, lambda m: f"{m.group(1)}{version}", original, count=1)

    if updated == original:
        marker = "program:\n  release:\n    version: "
        if marker not in original:
            raise RuntimeError("Could not find program.release.version in config file")
        updated = original.replace(marker, marker + version + "\n")

    if dry_run:
        return f"Dry run: would update {config_file} to version {version}"

    config_file.write_text(updated, encoding="utf-8")
    return f"Updated {config_file} to version {version}"


def ensure_release_post(repo: str, dry_run: bool = False, output_dir: str = "releases/_posts", config_path: str = "_config.yml") -> str:
    release = fetch_latest_release(repo)
    tag = release.get("tag_name")
    if not tag:
        raise RuntimeError("Latest GitHub release is missing a tag_name")

    published_at = release.get("published_at") or release.get("created_at") or ""
    published_date = published_at[:10] if published_at else date.today().isoformat()
    version = release_version(tag)
    filename = f"{published_date}-Release_{version}.md"
    target = Path(output_dir) / filename

    if target.exists():
        result = f"Skipping {target}: release already exists"
    else:
        post_contents = render_post(tag, published_at, release.get("body", ""))
        if dry_run:
            result = f"Dry run: would create {target}\n{post_contents}"
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(post_contents, encoding="utf-8")
            result = f"Created {target}"

    config_result = update_config_version(config_path, tag, dry_run=dry_run)
    return f"{result}\n{config_result}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync the latest Boomaga release notes into the Jekyll site.")
    parser.add_argument("--repo", default="Boomaga/boomaga", help="GitHub repository to read releases from")
    parser.add_argument("--output-dir", default="releases/_posts", help="Directory to store generated release posts")
    parser.add_argument("--config-file", default="_config.yml", help="Config file to update with the latest release version")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be created without writing files")
    args = parser.parse_args()

    try:
        print(ensure_release_post(args.repo, dry_run=args.dry_run, output_dir=args.output_dir, config_path=args.config_file))
        return 0
    except Exception as exc:  # pragma: no cover - CLI error handling
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
