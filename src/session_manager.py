"""Session management: timer, statistics, pause/resume, summary (FR-006, FR-007)."""

import time
from dataclasses import dataclass, field

from .posture_analyzer import PostureStatus


@dataclass
class SessionStats:
    """Accumulated posture statistics for a session."""

    total_frames: int = 0
    good_frames: int = 0
    bad_frames: int = 0
    neck_angle_sum: float = 0.0
    shoulder_angle_sum: float = 0.0
    torso_angle_sum: float = 0.0
    analyzed_frames: int = 0


class SessionManager:
    """Tracks session time, accumulates posture stats, and generates summaries."""

    def __init__(self):
        self._start_time: float = 0.0
        self._pause_start: float = 0.0
        self._total_paused: float = 0.0
        self._paused: bool = False
        self._running: bool = False
        self._stats = SessionStats()

    def start(self) -> None:
        """Start a new monitoring session."""
        self._start_time = time.time()
        self._total_paused = 0.0
        self._paused = False
        self._running = True
        self._stats = SessionStats()

    def toggle_pause(self) -> bool:
        """Toggle pause state. Returns True if now paused."""
        if self._paused:
            self._total_paused += time.time() - self._pause_start
            self._paused = False
        else:
            self._pause_start = time.time()
            self._paused = True
        return self._paused

    @property
    def is_paused(self) -> bool:
        return self._paused

    @property
    def is_running(self) -> bool:
        return self._running

    def elapsed_seconds(self) -> float:
        """Return active session time in seconds (excluding paused time)."""
        if not self._running:
            return 0.0
        now = time.time()
        paused = self._total_paused
        if self._paused:
            paused += now - self._pause_start
        return now - self._start_time - paused

    def elapsed_formatted(self) -> str:
        """Return elapsed time as HH:MM:SS."""
        total = int(self.elapsed_seconds())
        hours, remainder = divmod(total, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def record_frame(self, status: PostureStatus,
                     neck: float = 0.0, shoulder: float = 0.0,
                     torso: float = 0.0) -> None:
        """Record a single frame's posture classification and angles."""
        if self._paused:
            return
        self._stats.total_frames += 1
        if status == PostureStatus.GOOD:
            self._stats.good_frames += 1
        elif status == PostureStatus.BAD:
            self._stats.bad_frames += 1

        if status in (PostureStatus.GOOD, PostureStatus.BAD):
            self._stats.analyzed_frames += 1
            self._stats.neck_angle_sum += neck
            self._stats.shoulder_angle_sum += shoulder
            self._stats.torso_angle_sum += torso

    def stop(self) -> None:
        """Stop the session."""
        self._running = False

    def get_summary(self) -> str:
        """Generate a session summary string."""
        s = self._stats
        duration = self.elapsed_formatted()
        total = s.good_frames + s.bad_frames
        if total == 0:
            return (
                f"\n{'='*50}\n"
                f"  SESSION SUMMARY\n"
                f"{'='*50}\n"
                f"  Duration:       {duration}\n"
                f"  No posture data recorded.\n"
                f"{'='*50}\n"
            )

        good_pct = (s.good_frames / total) * 100
        bad_pct = (s.bad_frames / total) * 100

        # Convert frame counts to approximate time using session duration.
        elapsed = self.elapsed_seconds()
        good_time = elapsed * (s.good_frames / total)
        bad_time = elapsed * (s.bad_frames / total)

        avg_neck = s.neck_angle_sum / s.analyzed_frames if s.analyzed_frames else 0
        avg_shoulder = s.shoulder_angle_sum / s.analyzed_frames if s.analyzed_frames else 0
        avg_torso = s.torso_angle_sum / s.analyzed_frames if s.analyzed_frames else 0

        return (
            f"\n{'='*50}\n"
            f"  SESSION SUMMARY\n"
            f"{'='*50}\n"
            f"  Duration:             {duration}\n"
            f"  Good Posture Time:    {self._format_seconds(good_time)}\n"
            f"  Bad Posture Time:     {self._format_seconds(bad_time)}\n"
            f"  Good Posture:         {good_pct:.1f}%\n"
            f"  Bad Posture:          {bad_pct:.1f}%\n"
            f"{'─'*50}\n"
            f"  Avg Neck Angle:       {avg_neck:.1f} deg\n"
            f"  Avg Shoulder Angle:   {avg_shoulder:.1f} deg\n"
            f"  Avg Torso Angle:      {avg_torso:.1f} deg\n"
            f"{'='*50}\n"
        )

    @staticmethod
    def _format_seconds(seconds: float) -> str:
        total = int(seconds)
        h, remainder = divmod(total, 3600)
        m, s = divmod(remainder, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"
