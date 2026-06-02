"""Helper to load Snowflake credentials for evaluation from env or Streamlit secrets.

Behavior:
- Check environment variables first.
- If missing, attempt to read .streamlit/secrets.toml at project root.
- Populate missing SNOWFLAKE_* env vars so evaluation can reuse Streamlit secrets.

This only affects evaluation code and does not modify production logic.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Mapping


def _read_toml(path: Path) -> Mapping | None:
    try:
        import tomllib as _toml  # Python 3.11+
    except Exception:
        try:
            import toml as _toml  # type: ignore
        except Exception:
            return None

    try:
        with path.open("rb") as f:
            return _toml.load(f)
    except Exception:
        try:
            with path.open("r", encoding="utf-8") as f:
                return _toml.loads(f.read())
        except Exception:
            return None


def _flatten(d: Mapping, parent_key: str = "") -> dict:
    """Flatten nested dicts into a single-level dict with keys unchanged."""
    items: dict = {}
    for k, v in d.items():
        if isinstance(v, Mapping):
            items.update(_flatten(v, parent_key + k + "."))
        else:
            items[k] = v
    return items


SNOWFLAKE_KEYS = [
    "SNOWFLAKE_ACCOUNT",
    "SNOWFLAKE_USER",
    "SNOWFLAKE_PASSWORD",
    "SNOWFLAKE_WAREHOUSE",
    "SNOWFLAKE_ROLE",
    "SNOWFLAKE_PRIVATE_KEY",
]


def load_streamlit_secrets_into_env(project_root: Path | str) -> dict:
    """Load missing SNOWFLAKE_* env vars from .streamlit/secrets.toml if present.

    Returns a dict of values that were set (key -> value).
    """
    project_root = Path(project_root)
    set_values = {}

    # If all keys already present, nothing to do
    missing = [k for k in SNOWFLAKE_KEYS if not os.getenv(k)]
    if not missing:
        return {}

    secrets_path = project_root / ".streamlit" / "secrets.toml"
    if not secrets_path.exists():
        return {}

    data = _read_toml(secrets_path)
    if not data:
        return {}

    # Streamlit secrets can be nested; flatten and search for keys case-insensitively
    flat = _flatten(data) if isinstance(data, Mapping) else {}

    for key in SNOWFLAKE_KEYS:
        if os.getenv(key):
            continue

        # direct match
        if key in data:
            os.environ[key] = str(data[key])
            set_values[key] = os.environ[key]
            continue

        # check flattened keys and case-insensitive matches
        for k, v in flat.items():
            if k.upper() == key or k.upper().endswith(key):
                os.environ[key] = str(v)
                set_values[key] = os.environ[key]
                break

        # top-level search: case-insensitive
        if key not in set_values:
            for k, v in data.items():
                if isinstance(k, str) and k.upper() == key:
                    os.environ[key] = str(v)
                    set_values[key] = os.environ[key]
                    break

    return set_values
