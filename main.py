"""Real-Time Posture Analysis System - Main Entry Point.

Usage:
    python main.py                      # Use default config
    python main.py --config config.json # Use custom config file

Controls:
    q - Quit and show session summary
    p - Pause / Resume analysis
"""

import argparse
import logging
import sys
import time

import cv2

from src.config import Config
from src.display_manager import DisplayManager
from src.pose_detector import PoseDetector
from src.posture_analyzer import PostureAnalyzer, PostureStatus
from src.segment_measurer import measure_segments
from src.session_manager import SessionManager
from src.video_capture import VideoCapture

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Real-Time Posture Analysis System")
    parser.add_argument(
        "--config", type=str, default=None,
        help="Path to JSON config file (default: config.json in project root)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = Config.load(args.config)
    logger.info(
        "Config loaded: neck=%.1f, shoulder=%.1f, torso=%.1f",
        config.neck_threshold, config.shoulder_threshold, config.torso_threshold,
    )

    # Initialize modules.
    camera = VideoCapture(camera_index=config.camera_index)
    detector = PoseDetector()
    analyzer = PostureAnalyzer(config)
    display = DisplayManager()
    session = SessionManager()

    # Open camera.
    if not camera.open():
        print("ERROR: No camera detected. Please connect a webcam and restart.")
        return 1

    session.start()
    logger.info("Posture monitoring session started. Press 'q' to quit, 'p' to pause.")

    # Segment measurements update every 2 seconds, not every frame.
    cached_segments = []
    last_segment_time = 0.0
    SEGMENT_INTERVAL = 2.0

    try:
        while True:
            success, frame = camera.read_frame()
            if not success or frame is None:
                logger.warning("Failed to read frame, skipping.")
                continue

            # Detect pose and analyze posture (skip analysis if paused).
            if session.is_paused:
                from src.posture_analyzer import PostureResult
                posture = PostureResult(
                    status=PostureStatus.GOOD, angles=None, offending_angles=[],
                )
                landmarks = {}
            else:
                pose_result = detector.detect(frame)
                posture = analyzer.analyze(pose_result.landmarks, pose_result.detected)
                landmarks = pose_result.landmarks

                # Measure body segment lengths every 2 seconds.
                now = time.time()
                if now - last_segment_time >= SEGMENT_INTERVAL:
                    h, w = frame.shape[:2]
                    new_segments = measure_segments(
                        landmarks, w, h, config.shoulder_width_cm,
                    )
                    if new_segments:
                        cached_segments = new_segments
                        session.record_segments(new_segments)
                        last_segment_time = now

                # Record frame stats.
                if posture.angles:
                    session.record_frame(
                        posture.status,
                        neck=posture.angles.neck_inclination,
                        shoulder=posture.angles.shoulder_alignment,
                        torso=posture.angles.torso_hip_angle,
                    )
                else:
                    session.record_frame(posture.status)

            # Render overlays.
            annotated = display.render(
                frame, posture, landmarks,
                session.elapsed_formatted(),
                session.is_paused,
                segments=cached_segments,
            )

            cv2.imshow("Posture Analysis", annotated)

            # Handle keyboard input.
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            elif key == ord("p"):
                paused = session.toggle_pause()
                logger.info("Session %s.", "paused" if paused else "resumed")

    except KeyboardInterrupt:
        logger.info("Interrupted by user.")
    finally:
        session.stop()
        print(session.get_summary())
        detector.close()
        camera.release()

    return 0


if __name__ == "__main__":
    sys.exit(main())
