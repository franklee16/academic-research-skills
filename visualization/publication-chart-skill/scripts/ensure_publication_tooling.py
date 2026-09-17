#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib
import json
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence


@dataclass(frozen=True)
class PackageStatus:
    package: str
    available: bool
    version: str | None = None
    error: str | None = None


@dataclass(frozen=True)
class InstallPlan:
    installer: str
    command: tuple[str, ...]


DEFAULT_PACKAGES: tuple[str, ...] = ("pubfig", "pubtab")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Probe and force-install pubfig/pubtab into the active Python environment."
    )
    parser.add_argument(
        "--require",
        dest="packages",
        action="append",
        choices=DEFAULT_PACKAGES,
        help="Package that must be available. Defaults to pubfig + pubtab.",
    )
    parser.add_argument(
        "--prefer",
        choices=("auto", "uv", "pip"),
        default="auto",
        help="Installer selection policy. Default: auto.",
    )
    parser.add_argument(
        "--cwd",
        type=Path,
        default=Path.cwd(),
        help="Project directory used for uv-managed detection. Default: current directory.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON summary.",
    )
    return parser.parse_args()


def probe_package(package: str) -> PackageStatus:
    try:
        module = importlib.import_module(package)
    except Exception as exc:  # noqa: BLE001
        return PackageStatus(package=package, available=False, error=f"{type(exc).__name__}: {exc}")

    version = getattr(module, "__version__", None)
    return PackageStatus(package=package, available=True, version=str(version) if version else None)


def is_uv_managed(cwd: Path) -> bool:
    for candidate in [cwd, *cwd.parents]:
        if (candidate / "uv.lock").exists():
            return True
        pyproject = candidate / "pyproject.toml"
        if pyproject.exists():
            try:
                text = pyproject.read_text(encoding="utf-8")
            except OSError:
                continue
            if "[tool.uv" in text or "uv_build" in text:
                return True
    return False


def choose_installer(prefer: str, cwd: Path) -> str:
    if prefer in {"uv", "pip"}:
        return prefer
    if shutil.which("uv") and is_uv_managed(cwd):
        return "uv"
    return "pip"


def build_install_plan(installer: str, package: str) -> InstallPlan:
    if installer == "uv":
        command = ("uv", "pip", "install", "--python", sys.executable, package)
    else:
        command = (sys.executable, "-m", "pip", "install", package)
    return InstallPlan(installer=installer, command=command)


def run_command(command: Sequence[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=False, text=True, capture_output=True)


def emit_text(
    before: list[PackageStatus],
    after: list[PackageStatus],
    attempts: list[dict[str, object]],
) -> None:
    print("[publication-chart-skill] environment summary")
    print(f"python: {sys.executable}")
    print("before:")
    for status in before:
        suffix = f" ({status.version})" if status.version else ""
        detail = f" - {status.error}" if status.error else ""
        print(f"  - {status.package}: {'available' if status.available else 'missing'}{suffix}{detail}")
    if attempts:
        print("install attempts:")
        for attempt in attempts:
            print(f"  - {attempt['package']}: {attempt['command']} -> exit {attempt['returncode']}")
    print("after:")
    for status in after:
        suffix = f" ({status.version})" if status.version else ""
        detail = f" - {status.error}" if status.error else ""
        print(f"  - {status.package}: {'available' if status.available else 'missing'}{suffix}{detail}")


def main() -> int:
    args = parse_args()
    packages = tuple(dict.fromkeys(args.packages or DEFAULT_PACKAGES))
    before = [probe_package(package) for package in packages]
    missing = [status.package for status in before if not status.available]
    installer = choose_installer(args.prefer, args.cwd.resolve())

    attempts: list[dict[str, object]] = []
    for package in missing:
        plan = build_install_plan(installer=installer, package=package)
        result = run_command(plan.command)
        attempts.append(
            {
                "package": package,
                "installer": plan.installer,
                "command": " ".join(plan.command),
                "returncode": result.returncode,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
            }
        )

    after = [probe_package(package) for package in packages]
    payload = {
        "python": sys.executable,
        "installer": installer,
        "before": [asdict(status) for status in before],
        "attempts": attempts,
        "after": [asdict(status) for status in after],
        "ok": all(status.available for status in after),
    }

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        emit_text(before=before, after=after, attempts=attempts)

    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
