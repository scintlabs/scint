from __future__ import annotations

from attrs import define


@define
class Preferences:
    parts = []
    parts.append("## User Info")
    parts.append("Name: Tim")
