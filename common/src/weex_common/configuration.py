from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any


def _prefix(prefix: str) -> str:
    return prefix if prefix.endswith("_") else prefix + "_"


@dataclass(slots=True)
class ConfigurationRestAPI:
    base_path: str | None = None
    api_key: str | None = None
    api_secret: str | None = None
    passphrase: str | None = None
    timeout: float = 30.0
    max_retries: int = 0
    base_headers: dict[str, str] = field(default_factory=dict)
    user_agent: str | None = None
    session: Any = None

    @classmethod
    def from_env(
        cls,
        *,
        env_prefix: str = "WEEX_",
        base_url_env: str = "WEEX_BASE_URL",
    ) -> "ConfigurationRestAPI":
        prefix = _prefix(env_prefix)
        return cls(
            base_path=os.getenv(base_url_env, "").strip() or None,
            api_key=os.getenv(f"{prefix}API_KEY", "").strip() or None,
            api_secret=os.getenv(f"{prefix}API_SECRET", "").strip() or None,
            passphrase=os.getenv(f"{prefix}API_PASSPHRASE", "").strip() or None,
        )


@dataclass(slots=True)
class ConfigurationWebSocketAPI:
    stream_url: str | None = None
    api_key: str | None = None
    api_secret: str | None = None
    passphrase: str | None = None
    timeout: float = 30.0
    reconnect_delay: float = 1.5
    user_agent: str | None = None

    @classmethod
    def from_env(
        cls,
        *,
        env_prefix: str = "WEEX_",
        stream_url_env: str = "WEEX_WS_PRIVATE_URL",
    ) -> "ConfigurationWebSocketAPI":
        prefix = _prefix(env_prefix)
        return cls(
            stream_url=os.getenv(stream_url_env, "").strip() or None,
            api_key=os.getenv(f"{prefix}API_KEY", "").strip() or None,
            api_secret=os.getenv(f"{prefix}API_SECRET", "").strip() or None,
            passphrase=os.getenv(f"{prefix}API_PASSPHRASE", "").strip() or None,
        )


@dataclass(slots=True)
class ConfigurationWebSocketStreams:
    stream_url: str | None = None
    timeout: float = 30.0
    reconnect_delay: float = 1.5
    user_agent: str | None = None

    @classmethod
    def from_env(
        cls,
        *,
        stream_url_env: str = "WEEX_WS_PUBLIC_URL",
    ) -> "ConfigurationWebSocketStreams":
        return cls(stream_url=os.getenv(stream_url_env, "").strip() or None)
