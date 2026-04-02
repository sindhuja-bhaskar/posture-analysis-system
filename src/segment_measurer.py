"""Segment length measurement module: calculates body segment distances in cm."""

import math
from dataclasses import dataclass

from .pose_detector import Landmark


# Body segments: (start_landmark, end_landmark, display_label).
# Grouped by body region for readable overlay output.
SEGMENTS = [
    # --- Head / Neck ---
    ("nose", "left_ear", "Head Width (half)"),
    ("left_ear", "left_shoulder", "L Ear-Shoulder"),
    ("right_ear", "right_shoulder", "R Ear-Shoulder"),
    # --- Shoulders ---
    ("left_shoulder", "right_shoulder", "Between Shoulders"),
    # --- Arms ---
    ("left_shoulder", "left_elbow", "L Upper Arm"),
    ("right_shoulder", "right_elbow", "R Upper Arm"),
    ("left_elbow", "left_wrist", "L Forearm"),
    ("right_elbow", "right_wrist", "R Forearm"),
    ("left_wrist", "left_index", "L Hand"),
    ("right_wrist", "right_index", "R Hand"),
    ("left_shoulder", "left_index", "L Full Arm"),
    ("right_shoulder", "right_index", "R Full Arm"),
    # --- Torso ---
    ("left_shoulder", "left_hip", "L Torso"),
    ("right_shoulder", "right_hip", "R Torso"),
    ("left_hip", "right_hip", "Hip Width"),
    # --- Legs ---
    ("left_hip", "left_knee", "L Thigh"),
    ("right_hip", "right_knee", "R Thigh"),
    ("left_knee", "left_ankle", "L Shin"),
    ("right_knee", "right_ankle", "R Shin"),
    ("left_hip", "left_ankle", "L Full Leg"),
    ("right_hip", "right_ankle", "R Full Leg"),
    # --- Feet ---
    ("left_ankle", "left_heel", "L Ankle-Heel"),
    ("right_ankle", "right_heel", "R Ankle-Heel"),
    ("left_heel", "left_foot_index", "L Foot"),
    ("right_heel", "right_foot_index", "R Foot"),
    # --- Full height estimate ---
    ("nose", "left_ankle", "L Head-Ankle"),
    ("nose", "right_ankle", "R Head-Ankle"),
]

# Grouping for organized display in the info window.
SEGMENT_GROUPS: list[tuple[str, list[str]]] = [
    ("Head / Neck", ["Head Width (half)", "L Ear-Shoulder", "R Ear-Shoulder"]),
    ("Shoulders", ["Between Shoulders"]),
    ("Arms", ["L Upper Arm", "R Upper Arm", "L Forearm", "R Forearm",
              "L Hand", "R Hand", "L Full Arm", "R Full Arm"]),
    ("Torso", ["L Torso", "R Torso", "Hip Width"]),
    ("Legs", ["L Thigh", "R Thigh", "L Shin", "R Shin",
              "L Full Leg", "R Full Leg"]),
    ("Feet", ["L Ankle-Heel", "R Ankle-Heel", "L Foot", "R Foot"]),
    ("Height", ["L Head-Ankle", "R Head-Ankle"]),
]

# Minimum visibility to trust a landmark for measurement.
MIN_SEGMENT_VISIBILITY = 0.3


@dataclass
class SegmentLength:
    """A measured body segment."""

    label: str
    start_name: str
    end_name: str
    length_cm: float


def _pixel_distance(a: Landmark, b: Landmark, w: int, h: int) -> float:
    """Euclidean distance between two landmarks in pixel space."""
    dx = (a.x - b.x) * w
    dy = (a.y - b.y) * h
    return math.sqrt(dx * dx + dy * dy)


def measure_segments(
    landmarks: dict[str, Landmark],
    frame_w: int,
    frame_h: int,
    shoulder_width_cm: float,
) -> list[SegmentLength]:
    """Measure all body segments in cm.

    Uses the detected shoulder width (in pixels) and the user's actual
    shoulder_width_cm to compute a px-to-cm scale factor, then applies
    it to all other segments.
    """
    ls = landmarks.get("left_shoulder")
    rs = landmarks.get("right_shoulder")
    if ls is None or rs is None:
        return []

    shoulder_px = _pixel_distance(ls, rs, frame_w, frame_h)
    if shoulder_px < 1.0:
        return []

    px_to_cm = shoulder_width_cm / shoulder_px

    results: list[SegmentLength] = []
    for start_name, end_name, label in SEGMENTS:
        a = landmarks.get(start_name)
        b = landmarks.get(end_name)
        if a is None or b is None:
            continue
        if a.visibility < MIN_SEGMENT_VISIBILITY or b.visibility < MIN_SEGMENT_VISIBILITY:
            continue
        dist_px = _pixel_distance(a, b, frame_w, frame_h)
        length_cm = dist_px * px_to_cm
        results.append(SegmentLength(
            label=label, start_name=start_name, end_name=end_name,
            length_cm=round(length_cm, 1),
        ))

    return results
