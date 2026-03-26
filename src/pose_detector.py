"""Pose detection module using MediaPipe Pose (FR-002)."""

import logging
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import cv2
import mediapipe as mp
import numpy as np

logger = logging.getLogger(__name__)

PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
PoseLandmarkEnum = mp.tasks.vision.PoseLandmark
RunningMode = mp.tasks.vision.RunningMode
BaseOptions = mp.tasks.BaseOptions

MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "pose_landmarker/pose_landmarker_lite/float16/latest/"
    "pose_landmarker_lite.task"
)
MODEL_PATH = Path(__file__).resolve().parent.parent / "pose_landmarker.task"


@dataclass
class Landmark:
    """A single body landmark with coordinates and visibility."""

    x: float
    y: float
    z: float
    visibility: float


@dataclass
class PoseResult:
    """Result of pose detection for a single frame."""

    landmarks: dict[str, Landmark]
    detected: bool


# Landmark indices we care about for posture analysis.
LANDMARK_INDICES = {
    "nose": PoseLandmarkEnum.NOSE,
    "left_ear": PoseLandmarkEnum.LEFT_EAR,
    "right_ear": PoseLandmarkEnum.RIGHT_EAR,
    "left_shoulder": PoseLandmarkEnum.LEFT_SHOULDER,
    "right_shoulder": PoseLandmarkEnum.RIGHT_SHOULDER,
    "left_hip": PoseLandmarkEnum.LEFT_HIP,
    "right_hip": PoseLandmarkEnum.RIGHT_HIP,
}


def _ensure_model() -> Path:
    """Download the pose landmarker model if not already present."""
    if MODEL_PATH.exists():
        return MODEL_PATH
    logger.info("Downloading pose landmarker model to %s ...", MODEL_PATH)
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    logger.info("Model downloaded successfully.")
    return MODEL_PATH


class PoseDetector:
    """Detects human body landmarks in video frames using MediaPipe Pose."""

    def __init__(self, min_detection_confidence: float = 0.5,
                 min_tracking_confidence: float = 0.5):
        model_path = _ensure_model()
        options = PoseLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=str(model_path)),
            running_mode=RunningMode.VIDEO,
            min_pose_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )
        self._landmarker = PoseLandmarker.create_from_options(options)
        self._frame_timestamp_ms = 0

    def detect(self, frame: np.ndarray) -> PoseResult:
        """Process a BGR frame and return detected landmarks."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        self._frame_timestamp_ms += 33  # ~30 FPS timestamp increment
        results = self._landmarker.detect_for_video(mp_image, self._frame_timestamp_ms)

        if not results.pose_landmarks or len(results.pose_landmarks) == 0:
            return PoseResult(landmarks={}, detected=False)

        pose_landmarks = results.pose_landmarks[0]
        landmarks = {}
        for name, index in LANDMARK_INDICES.items():
            lm = pose_landmarks[index]
            landmarks[name] = Landmark(
                x=lm.x, y=lm.y, z=lm.z, visibility=lm.visibility,
            )

        return PoseResult(landmarks=landmarks, detected=True)

    def close(self) -> None:
        """Release MediaPipe resources."""
        self._landmarker.close()
