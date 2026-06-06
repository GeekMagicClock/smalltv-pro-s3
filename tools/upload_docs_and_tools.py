#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


DEFAULT_REPO = "GeekMagicClock/smalltv-pro-s3"
IGNORE_PATTERNS = ("__pycache__", "*.pyc", ".DS_Store")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Upload the local docs/ and tools/ folders to the GeekMagicClock release repo."
    )
    parser.add_argument(
        "--repo",
        default=DEFAULT_REPO,
        help=f"Target GitHub repo slug. Default: {DEFAULT_REPO}",
    )
    parser.add_argument(
        "--branch",
        default="main",
        help="Target branch name. Default: main",
    )
    parser.add_argument(
        "--transport",
        choices=("https", "ssh"),
        default="ssh",
        help="Git transport to use. Default: ssh",
    )
    parser.add_argument(
        "--message",
        default="Upload docs and tools",
        help="Git commit message. Default: 'Upload docs and tools'",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Prepare files and show the final uploader command without pushing.",
    )
    return parser.parse_args()


def copy_tree(src: Path, dst: Path) -> None:
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns(*IGNORE_PATTERNS))


def main() -> int:
    args = parse_args()
    project_root = Path(__file__).resolve().parents[1]
    docs_src = project_root / "docs"
    tools_src = project_root / "tools"
    uploader = project_root / "scripts" / "github_repo_uploader.py"

    if not docs_src.is_dir():
        print(f"ERROR: docs directory not found: {docs_src}", file=sys.stderr)
        return 1
    if not tools_src.is_dir():
        print(f"ERROR: tools directory not found: {tools_src}", file=sys.stderr)
        return 1
    if not uploader.is_file():
        print(f"ERROR: uploader script not found: {uploader}", file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory(prefix="upload_docs_tools_") as tmp_dir:
        stage_root = Path(tmp_dir)
        staged_docs = stage_root / "docs"
        staged_tools = stage_root / "tools"
        copy_tree(docs_src, staged_docs)
        copy_tree(tools_src, staged_tools)

        cmd = [
            sys.executable,
            str(uploader),
            "--repo",
            args.repo,
            "--branch",
            args.branch,
            "--transport",
            args.transport,
            "--message",
            args.message,
            "--item",
            f"{staged_docs}=docs",
            "--item",
            f"{staged_tools}=tools",
        ]
        if args.dry_run:
            cmd.append("--dry-run")

        print("Running uploader command:")
        print(" ".join(cmd))
        result = subprocess.run(cmd, cwd=project_root)
        return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
