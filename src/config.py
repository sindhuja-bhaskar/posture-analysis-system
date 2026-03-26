"""Configuration loader with validation and defaults fallback (FR-008)."""

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path

logger = logging.getLogger(__name__)

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.json"

DEFAULTS = {
    "neck_threshold": 25.0,
    "shoulder_threshold": 10.0,
    "torso_threshold": 20.0,
    "min_visibility_confidence": 0.5,
    "camera_index": 0,
}


@dataclass
class Config:
    """Posture analysis configuration with validated thresholds."""

    neck_threshold: float = DEFAULTS["neck_threshold"]
    shoulder_threshold: float = DEFAULTS["shoulder_threshold"]
    torso_threshold: float = DEFAULTS["torso_threshold"]
    min_visibility_confidence: float = DEFAULTS["min_visibility_confidence"]
    camera_index: int = DEFAULTS["camera_index"]

    @classmethod
    def load(cls, path: str | Path | None = None) -> "Config":
        """Load config from JSON file. Falls back to defaults on error."""
        config_path = Path(path) if path else DEFAULT_CONFIG_PATH

        if not config_path.exists():
            logger.info("No config file found at %s, using defaults.", config_path)
            return cls()

        try:
            with open(config_path, "r") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            logger.warning("Failed to read config file: %s. Using defaults.", e)
            return cls()

        validated = {}
        for key, default in DEFAULTS.items():
            if key not in data:
                continue
            value = data[key]
            if not cls._validate_field(key, value):
                logger.warning(
                    "Invalid value for '%s': %s. Using default: %s.",
                    key, value, default,
                )
                continue
            validated[key] = type(default)(value)

        return cls(**validated)

    @staticmethod
    def _validate_field(key: str, value) -> bool:
        """Validate a single config field value."""
        if key == "camera_index":
            return isinstance(value, int) and value >= 0
        if key == "min_visibility_confidence":
            return isinstance(value, (int, float)) and 0 <= value <= 1
        # Angle thresholds must be positive numbers
        return isinstance(value, (int, float)) and value > 0
