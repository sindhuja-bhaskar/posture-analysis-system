"""Video capture module for webcam frame acquisition (FR-001)."""

import logging
import cv2

logger = logging.getLogger(__name__)


class VideoCapture:
    """Manages webcam initialization, frame capture, and resource release."""

    def __init__(self, camera_index: int = 0):
        self._camera_index = camera_index
        self._cap: cv2.VideoCapture | None = None

    def open(self) -> bool:
        """Initialize the webcam. Returns True if successful."""
        self._cap = cv2.VideoCapture(self._camera_index)
        if not self._cap.isOpened():
            logger.error(
                "No camera detected. Please connect a webcam and restart."
            )
            self._cap = None
            return False
        logger.info(
            "Camera opened: %.0fx%.0f @ %.0f FPS",
            self._cap.get(cv2.CAP_PROP_FRAME_WIDTH),
            self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT),
            self._cap.get(cv2.CAP_PROP_FPS),
        )
        return True

    def read_frame(self):
        """Capture a single frame. Returns (success, frame)."""
        if self._cap is None:
            return False, None
        return self._cap.read()

    def release(self) -> None:
        """Release the webcam and destroy OpenCV windows."""
        if self._cap is not None:
            self._cap.release()
            self._cap = None
        cv2.destroyAllWindows()
        logger.info("Camera released and windows closed.")

    @property
    def is_opened(self) -> bool:
        return self._cap is not None and self._cap.isOpened()
