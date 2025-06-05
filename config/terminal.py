from __future__ import annotations

import os
import platform
import subprocess
import asyncio
from pathlib import Path
from typing import Dict, List


async def use_terminal(command: str):
    process = await asyncio.create_subprocess_shell(
        command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    output = stdout.decode().strip() if stdout else ""
    errors = stderr.decode().strip() if stderr else ""
    if errors:
        return process.returncode == 0, {"output": output, "errors": errors}
    return True, output


def _safe_run(cmd: List[str]) -> str | None:
    try:
        return subprocess.check_output(cmd, text=True).strip()
    except Exception:
        return None


def _docker_snapshot() -> List[Dict[str, str]]:
    ps = _safe_run(["docker", "ps", "--format", "{{.Names}};{{.Status}};{{.Ports}}"])
    if not ps:
        return []
    out = []
    for line in ps.splitlines():
        name, status, ports = line.split(";", maxsplit=2)
        out.append({"name": name, "status": status, "ports": ports or ""})
    return out


def _dir_tree(root: Path, depth: int = 2) -> List[str]:
    items, queue = [], [(root, 0)]
    while queue and len(items) < 50:
        path, lvl = queue.pop(0)
        rel = path.relative_to(root).as_posix() or "."
        items.append(rel + ("/" if path.is_dir() else ""))
        if lvl < depth and path.is_dir():
            queue += [(p, lvl + 1) for p in sorted(path.iterdir())]
    return items


def gather_context(
    cwd: Path | str = Path.cwd(),
    allowed_cmds: List[str] | None = None,
    network_allowed: bool = False,
    sudo: bool = False,
    depth: int = 2,
):
    cwd = Path(cwd).resolve()
    allowed_cmds = allowed_cmds or ["ls", "cat", "grep", "git", "docker"]
    ctx: Dict[str, object] = {
        "context_version": "1.0",
        "os": platform.system().lower(),
        "distro": _safe_run(["lsb_release", "-sd"]) or platform.platform(),
        "kernel": platform.release(),
        "arch": platform.machine(),
        "user": os.getenv("USER") or os.getenv("USERNAME"),
        "shell": os.getenv("SHELL")
        or _safe_run(["ps", "-p", str(os.getppid()), "-o", "comm="]),
        "python": platform.python_version(),
        "cwd": str(cwd),
        "allowed_commands": allowed_cmds,
        "network": "outbound" if network_allowed else "outbound-blocked",
        "sudo": sudo,
        "env": {
            "PATH": os.getenv("PATH"),
            "VIRTUAL_ENV": os.getenv("VIRTUAL_ENV", ""),
        },
        "snapshot": {
            "files": _dir_tree(cwd, depth=depth),
            "containers": _docker_snapshot(),
        },
    }
    return ctx


if __name__ == "__main__":
    context = gather_context()
    print(context)
