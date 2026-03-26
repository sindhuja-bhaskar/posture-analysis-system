"""Posture analysis module: angle calculation and classification (FR-003, FR-004)."""

import math
from dataclasses import dataclass
from enum import Enum

from .config import Config
from .pose_detector import Landmark


class PostureStatus(Enum):
    GOOD = "Good Posture"
    BAD = "Bad Posture"
    LOW_CONFIDENCE = "Low Confidence -- Unable to Classify"
    NO_PERSON = "No person detected"


@dataclass
class AngleResult:
    """Calculated body angles in degrees."""

    neck_inclination: float
    shoulder_alignment: float
    torso_hip_angle: float


@dataclass
class PostureResult:
    """Complete posture analysis result for a single frame."""

    status: PostureStatus
    angles: AngleResult | None
    offending_angles: list[str]


class PostureAnalyzer:
    """Calculates body angles from landmarks and classifies posture."""

    def __init__(self, config: Config):
        self._config = config

    def analyze(self, landmarks: dict[str, Landmark], detected: bool) -> PostureResult:
        """Analyze posture from detected landmarks."""
        if not detected or not landmarks:
            return PostureResult(
                status=PostureStatus.NO_PERSON, angles=None, offending_angles=[],
            )

        # Check confidence for key landmarks.
        # Upper-body landmarks (ears, shoulders) use visibility check.
        # Hip landmarks often report low visibility when partially occluded
        # by a desk/chair, but MediaPipe still returns usable coordinates,
        # so we only require that they are present (not None).
        confidence_required = ["left_shoulder", "right_shoulder",
                               "left_ear", "right_ear"]
        presence_required = ["left_hip", "right_hip"]

        for name in presence_required:
            if landmarks.get(name) is None:
                return PostureResult(
                    status=PostureStatus.LOW_CONFIDENCE,
                    angles=None,
                    offending_angles=[],
                )

        for name in confidence_required:
            lm = landmarks.get(name)
            if lm is None or lm.visibility < self._config.min_visibility_confidence:
                return PostureResult(
                    status=PostureStatus.LOW_CONFIDENCE,
                    angles=None,
                    offending_angles=[],
                )

        angles = self._calculate_angles(landmarks)
        offending = self._check_thresholds(angles)

        status = PostureStatus.BAD if offending else PostureStatus.GOOD
        return PostureResult(status=status, angles=angles, offending_angles=offending)

    def _calculate_angles(self, lm: dict[str, Landmark]) -> AngleResult:
        """Compute neck inclination, shoulder alignment, and torso-hip angle."""
        # Neck inclination: angle between midpoint(ears)-midpoint(shoulders) vector and vertical.
        mid_ear = self._midpoint(lm["left_ear"], lm["right_ear"])
        mid_shoulder = self._midpoint(lm["left_shoulder"], lm["right_shoulder"])
        neck_inclination = self._angle_with_vertical(
            mid_ear.x - mid_shoulder.x,
            mid_ear.y - mid_shoulder.y,
        )

        # Shoulder alignment: deviation of shoulder line from horizontal.
        shoulder_dx = lm["right_shoulder"].x - lm["left_shoulder"].x
        shoulder_dy = lm["right_shoulder"].y - lm["left_shoulder"].y
        shoulder_alignment = abs(math.degrees(math.atan2(shoulder_dy, shoulder_dx)))
        # Normalize: 0 means perfectly horizontal.
        shoulder_alignment = abs(shoulder_alignment) if shoulder_alignment <= 90 else abs(180 - shoulder_alignment)

        # Torso-hip angle: angle of midpoint(shoulders)-midpoint(hips) vector from vertical.
        mid_hip = self._midpoint(lm["left_hip"], lm["right_hip"])
        torso_hip_angle = self._angle_with_vertical(
            mid_shoulder.x - mid_hip.x,
            mid_shoulder.y - mid_hip.y,
        )

        return AngleResult(
            neck_inclination=round(neck_inclination, 1),
            shoulder_alignment=round(shoulder_alignment, 1),
            torso_hip_angle=round(torso_hip_angle, 1),
        )

    def _check_thresholds(self, angles: AngleResult) -> list[str]:
        """Return list of angle names exceeding their thresholds."""
        offending = []
        if angles.neck_inclination > self._config.neck_threshold:
            offending.append("neck_inclination")
        if angles.shoulder_alignment > self._config.shoulder_threshold:
            offending.append("shoulder_alignment")
        if angles.torso_hip_angle > self._config.torso_threshold:
            offending.append("torso_hip_angle")
        return offending

    @staticmethod
    def _midpoint(a: Landmark, b: Landmark) -> Landmark:
        """Return the midpoint of two landmarks."""
        return Landmark(
            x=(a.x + b.x) / 2,
            y=(a.y + b.y) / 2,
            z=(a.z + b.z) / 2,
            visibility=min(a.visibility, b.visibility),
        )

    @staticmethod
    def _angle_with_vertical(dx: float, dy: float) -> float:
        """Calculate angle (degrees) between a vector (dx, dy) and the vertical axis.

        In image coordinates y increases downward, so vertical-up is (0, -1).
        Returns angle in range [0, 180].
        """
        # Vertical reference: (0, -1) in image coordinates (upward).
        angle = math.degrees(math.atan2(dx, -dy))
        return abs(angle)
