#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import tempfile
import subprocess
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
WINDOWS_APP_DIR = ROOT / "windows_app"
WINDOWS_DOWNLOAD_ZIP = ROOT / "ER_prooftool_windows_app.zip"
WINDOWS_ZIP = ROOT / "windows_app.zip"

WINDOWS_APP_FILES = [
    "README_WINDOWS.txt",
    "Setup DOCX Compare App.bat",
    "Start DOCX Compare App.bat",
    "compare_ui.html",
    "compare_ui_server.py",
    "generate_diff_pdf.py",
    "launch_compare_app.py",
    "quality_check_pdf_compare.py",
    "requirements.txt",
    "setup_windows.py",
    "ui_runs/.gitkeep",
]

def build_windows_zip(zip_path: Path) -> None:
    missing = [rel for rel in WINDOWS_APP_FILES if not (WINDOWS_APP_DIR / rel).exists()]
    if missing:
        raise FileNotFoundError(f"Missing Windows app files: {missing}")

    temp_dir = Path(tempfile.mkdtemp(prefix="windows_zip_stage_"))
    try:
        stage_root = temp_dir / "windows_app"
        stage_root.mkdir(parents=True, exist_ok=True)
        for rel in WINDOWS_APP_FILES:
            src = WINDOWS_APP_DIR / rel
            dest = stage_root / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)

        zip_path.parent.mkdir(parents=True, exist_ok=True)
        if zip_path.exists():
            zip_path.unlink()

        subprocess.run(
            ["/usr/bin/zip", "-r", "-X", str(zip_path), "windows_app"],
            cwd=temp_dir,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def validate_windows_zip(zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()
        if any("__pycache__" in name for name in names):
            raise RuntimeError("Windows ZIP still contains __pycache__ content.")

    temp_dir = Path(tempfile.mkdtemp(prefix="windows_zip_verify_"))
    try:
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(temp_dir)
        extracted_server = temp_dir / "windows_app" / "compare_ui_server.py"
        if not extracted_server.exists():
            raise RuntimeError("Validation extract did not produce the Windows server file.")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a Windows-friendly ZIP bundle for the compare app.")
    parser.add_argument(
        "--output",
        type=Path,
        default=WINDOWS_DOWNLOAD_ZIP,
        help="Path to the primary output zip file.",
    )
    parser.add_argument("--skip-validate", action="store_true", help="Skip post-build validation.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    primary_output = args.output
    build_windows_zip(primary_output)
    if not args.skip_validate:
        validate_windows_zip(primary_output)

    if primary_output.resolve() != WINDOWS_ZIP.resolve():
        shutil.copyfile(primary_output, WINDOWS_ZIP)
        if not args.skip_validate:
            validate_windows_zip(WINDOWS_ZIP)
        print(f"Built Windows ZIPs: {primary_output} and {WINDOWS_ZIP}")
    else:
        print(f"Built Windows ZIP: {primary_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
