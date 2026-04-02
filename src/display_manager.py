"""Display manager: overlay rendering, color-coded feedback, FPS counter (FR-005, FR-009)."""

import time

import cv2
import numpy as np

from .pose_detector import Landmark
from .posture_analyzer import AngleResult, PostureResult, PostureStatus
from .segment_measurer import SEGMENT_GROUPS, SegmentLength

# Colors (BGR).
GREEN = (0, 200, 0)
RED = (0, 0, 220)
YELLOW = (0, 220, 220)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)

# Skeletal connections for visualization (pairs of landmark names).
SKELETON_CONNECTIONS = [
    # Head-neck
    ("nose", "left_ear"),
    ("nose", "right_ear"),
    ("left_ear", "left_shoulder"),
    ("right_ear", "right_shoulder"),
    # Shoulders
    ("left_shoulder", "right_shoulder"),
    # Arms
    ("left_shoulder", "left_elbow"),
    ("right_shoulder", "right_elbow"),
    ("left_elbow", "left_wrist"),
    ("right_elbow", "right_wrist"),
    ("left_wrist", "left_index"),
    ("right_wrist", "right_index"),
    # Torso
    ("left_shoulder", "left_hip"),
    ("right_shoulder", "right_hip"),
    ("left_hip", "right_hip"),
    # Legs
    ("left_hip", "left_knee"),
    ("right_hip", "right_knee"),
    ("left_knee", "left_ankle"),
    ("right_knee", "right_ankle"),
    # Feet
    ("left_ankle", "left_heel"),
    ("right_ankle", "right_heel"),
    ("left_heel", "left_foot_index"),
    ("right_heel", "right_foot_index"),
    ("left_ankle", "left_foot_index"),
    ("right_ankle", "right_foot_index"),
]

FONT = cv2.FONT_HERSHEY_SIMPLEX


class DisplayManager:
    """Renders overlays on video frames: landmarks, skeleton, labels, angles, FPS."""

    # Info window layout constants.
    _INFO_W = 420
    _LINE_H = 22
    _MARGIN = 15
    _CYAN = (200, 200, 0)

    def __init__(self):
        self._prev_time: float = time.time()
        self._fps: float = 0.0
        self._last_segments: list[SegmentLength] | None = None

    def render(self, frame: np.ndarray, posture: PostureResult,
               landmarks: dict[str, Landmark],
               elapsed: str, paused: bool,
               segments: list[SegmentLength] | None = None) -> np.ndarray:
        """Compose all overlays onto the frame and return the annotated frame."""
        self._update_fps()
        h, w = frame.shape[:2]

        if landmarks:
            self._draw_skeleton(frame, landmarks, w, h, posture.offending_angles)
            self._draw_landmarks(frame, landmarks, w, h)

        self._draw_status_label(frame, posture.status)
        self._show_info_window(posture, segments)
        self._draw_hud(frame, elapsed, paused)

        return frame

    def _update_fps(self) -> None:
        now = time.time()
        dt = now - self._prev_time
        self._fps = 1.0 / dt if dt > 0 else 0.0
        self._prev_time = now

    def _draw_landmarks(self, frame: np.ndarray,
                        landmarks: dict[str, Landmark],
                        w: int, h: int) -> None:
        """Draw circles at each detected landmark."""
        for lm in landmarks.values():
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(frame, (cx, cy), 5, GREEN, -1)
            cv2.circle(frame, (cx, cy), 6, WHITE, 1)

    def _draw_skeleton(self, frame: np.ndarray,
                       landmarks: dict[str, Landmark],
                       w: int, h: int,
                       offending: list[str]) -> None:
        """Draw skeletal connections between landmarks."""
        # Determine which connections should be highlighted red.
        red_connections = set()
        if "neck_inclination" in offending:
            red_connections.update([
                ("left_ear", "left_shoulder"),
                ("right_ear", "right_shoulder"),
            ])
        if "shoulder_alignment" in offending:
            red_connections.add(("left_shoulder", "right_shoulder"))
        if "torso_hip_angle" in offending:
            red_connections.update([
                ("left_shoulder", "left_hip"),
                ("right_shoulder", "right_hip"),
            ])

        for a_name, b_name in SKELETON_CONNECTIONS:
            a = landmarks.get(a_name)
            b = landmarks.get(b_name)
            if a is None or b is None:
                continue
            pt1 = (int(a.x * w), int(a.y * h))
            pt2 = (int(b.x * w), int(b.y * h))
            color = RED if (a_name, b_name) in red_connections else GREEN
            cv2.line(frame, pt1, pt2, color, 2)

    def _draw_status_label(self, frame: np.ndarray,
                           status: PostureStatus) -> None:
        """Draw the posture classification label at the top-center."""
        h, w = frame.shape[:2]
        label = status.value
        color = self._status_color(status)

        # Background rectangle for readability.
        text_size = cv2.getTextSize(label, FONT, 1.0, 2)[0]
        tx = (w - text_size[0]) // 2
        ty = 40
        cv2.rectangle(frame, (tx - 10, ty - 30), (tx + text_size[0] + 10, ty + 10),
                       (0, 0, 0), -1)
        cv2.putText(frame, label, (tx, ty), FONT, 1.0, color, 2, cv2.LINE_AA)

    def _show_info_window(self, posture: PostureResult,
                          segments: list[SegmentLength] | None) -> None:
        """Render posture angles and body segments in a separate window."""
        # Cache segments so we keep showing the last known values.
        if segments:
            self._last_segments = segments
        segs = self._last_segments

        # Count total lines to compute canvas height.
        # Posture section: title + 3 angle lines + 1 blank.
        line_count = 5
        if segs:
            # Segments section: title + per-group (header + items) + blank between groups.
            seg_lookup = {s.label: s.length_cm for s in segs}
            line_count += 1  # section title
            for group_name, labels in SEGMENT_GROUPS:
                visible = [l for l in labels if l in seg_lookup]
                if visible:
                    line_count += 1 + len(visible) + 1  # header + items + gap

        canvas_h = self._MARGIN * 2 + line_count * self._LINE_H
        canvas = np.zeros((canvas_h, self._INFO_W, 3), dtype=np.uint8)

        y = self._MARGIN + self._LINE_H
        x = self._MARGIN

        # --- Posture Angles ---
        cv2.putText(canvas, "Posture Angles", (x, y),
                    FONT, 0.6, YELLOW, 1, cv2.LINE_AA)
        y += self._LINE_H

        if posture.angles:
            offending = posture.offending_angles
            for name, value, key in [
                ("Neck", f"{posture.angles.neck_inclination:.0f} deg", "neck_inclination"),
                ("Shoulder", f"{posture.angles.shoulder_alignment:.0f} deg", "shoulder_alignment"),
                ("Torso", f"{posture.angles.torso_hip_angle:.0f} deg", "torso_hip_angle"),
            ]:
                color = RED if key in offending else GREEN
                cv2.putText(canvas, f"  {name}: {value}", (x, y),
                            FONT, 0.5, color, 1, cv2.LINE_AA)
                y += self._LINE_H
        else:
            cv2.putText(canvas, "  Waiting for detection...", (x, y),
                        FONT, 0.45, GRAY, 1, cv2.LINE_AA)
            y += self._LINE_H * 3

        y += self._LINE_H  # blank separator

        # --- Body Segments ---
        if segs:
            seg_lookup = {s.label: s.length_cm for s in segs}
            cv2.putText(canvas, "Body Segments (cm)", (x, y),
                        FONT, 0.6, YELLOW, 1, cv2.LINE_AA)
            y += self._LINE_H

            for group_name, labels in SEGMENT_GROUPS:
                visible = [(l, seg_lookup[l]) for l in labels if l in seg_lookup]
                if not visible:
                    continue
                # Group header with underline.
                cv2.putText(canvas, group_name, (x, y),
                            FONT, 0.5, self._CYAN, 1, cv2.LINE_AA)
                cv2.line(canvas, (x, y + 4), (x + 180, y + 4), GRAY, 1)
                y += self._LINE_H
                for label, length in visible:
                    cv2.putText(canvas, f"  {label}: {length:.1f}", (x, y),
                                FONT, 0.45, WHITE, 1, cv2.LINE_AA)
                    y += self._LINE_H
                y += 4  # small gap between groups

        cv2.imshow("Posture Info", canvas)

    def _draw_hud(self, frame: np.ndarray, elapsed: str, paused: bool) -> None:
        """Draw FPS counter, session timer, and pause indicator."""
        h, w = frame.shape[:2]

        # FPS - top-right.
        fps_text = f"FPS: {self._fps:.0f}"
        cv2.putText(frame, fps_text, (w - 130, 30), FONT, 0.6, WHITE, 1, cv2.LINE_AA)

        # Session timer - bottom-left.
        cv2.putText(frame, elapsed, (10, h - 20), FONT, 0.7, WHITE, 2, cv2.LINE_AA)

        # Pause indicator - center.
        if paused:
            pause_text = "PAUSED"
            text_size = cv2.getTextSize(pause_text, FONT, 1.5, 3)[0]
            tx = (w - text_size[0]) // 2
            ty = h // 2
            cv2.rectangle(frame, (tx - 15, ty - 45), (tx + text_size[0] + 15, ty + 15),
                           (0, 0, 0), -1)
            cv2.putText(frame, pause_text, (tx, ty), FONT, 1.5, YELLOW, 3, cv2.LINE_AA)

    @staticmethod
    def _status_color(status: PostureStatus) -> tuple:
        if status == PostureStatus.GOOD:
            return GREEN
        if status == PostureStatus.BAD:
            return RED
        return YELLOW
