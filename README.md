# Real-Time Posture Analysis System

A desktop application that uses your webcam and computer vision to monitor your sitting/standing posture in real time. It detects body landmarks using MediaPipe Pose, calculates joint angles, and classifies your posture as **Good** or **Bad** with color-coded visual feedback.

---

## Features

- Real-time body landmark detection and skeletal overlay
- Posture classification (Good/Bad) based on neck, shoulder, and torso angles
- Color-coded feedback: green for good posture, red for bad posture
- Angle values displayed on screen with threshold violation highlighting
- Session timer with pause/resume support
- Session summary with posture statistics and average angles
- Configurable angle thresholds via JSON config file
- FPS counter for performance monitoring
- Zero data persistence -- no video is recorded or stored

---

## Prerequisites

- **Python 3.9+** installed on your system
- A **webcam** (built-in or USB)
- **Operating System**: macOS 12+, Windows 10+, or Ubuntu 20.04+

---

## Installation & Setup

### macOS

#### 1. Install Python (if not already installed)

Check if Python is installed:

```bash
python3 --version
```

If not installed, install via Homebrew or download from [python.org](https://www.python.org/downloads/):

```bash
brew install python
```

#### 2. Clone or download the project

```bash
cd /path/to/your/projects
git clone <repository-url> posture-analysis-system
cd posture-analysis-system
```

#### 3. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the beginning of your terminal prompt.

#### 4. Install dependencies

```bash
pip install -r requirements.txt
```

#### 5. Grant camera permission

macOS blocks camera access by default for terminal apps. Before running the application:

1. Go to **System Settings > Privacy & Security > Camera**.
2. Enable the toggle for your terminal app (**Terminal**, **iTerm2**, **VS Code**, etc.).
3. If your terminal app does not appear in the list, run the app once so macOS registers it, then check again.
4. **Restart your terminal app** after granting permission.

> **VS Code users**: Grant camera access to **Visual Studio Code** specifically in the privacy settings.

#### 6. Run the application

```bash
python main.py
```

#### Quick reference (full macOS setup in one go)

```bash
cd posture-analysis-system
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

---

### Windows

#### 1. Install Python (if not already installed)

Download and install Python 3.9+ from [python.org](https://www.python.org/downloads/).

> **Important**: During installation, check the box **"Add Python to PATH"**.

Verify the installation by opening **Command Prompt** or **PowerShell**:

```cmd
python --version
```

#### 2. Clone or download the project

```cmd
cd C:\path\to\your\projects
git clone <repository-url> posture-analysis-system
cd posture-analysis-system
```

Or download and extract the ZIP file, then `cd` into the folder.

#### 3. Create a virtual environment

```cmd
python -m venv venv
```

#### 4. Activate the virtual environment

**Command Prompt:**

```cmd
venv\Scripts\activate
```

**PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

> **PowerShell execution policy error?** Run this first:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

You should see `(venv)` at the beginning of your terminal prompt.

#### 5. Install dependencies

```cmd
pip install -r requirements.txt
```

#### 6. Grant camera permission

Windows may prompt you to allow camera access on first run. If the camera does not work:

1. Go to **Settings > Privacy & Security > Camera**.
2. Make sure **Camera access** is turned **On**.
3. Scroll down and ensure **"Let desktop apps access your camera"** is turned **On**.

#### 7. Run the application

```cmd
python main.py
```

#### Quick reference (full Windows setup in one go)

**Command Prompt:**

```cmd
cd posture-analysis-system
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

**PowerShell:**

```powershell
cd posture-analysis-system
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

---

## Running the Application

Make sure your virtual environment is activated, then run:

| OS      | Command         |
|---------|-----------------|
| macOS   | `python main.py`  |
| Windows | `python main.py`  |

A window titled **"Posture Analysis"** will open showing your webcam feed with posture overlays.

The pose landmarker model (~4 MB) is downloaded automatically on the first run.

### Using a custom config file

```bash
python main.py --config path/to/your/config.json
```

---

## Controls

| Key | Action                                    |
|-----|-------------------------------------------|
| `q` | Quit the application and show session summary |
| `p` | Pause / Resume posture analysis           |

---

## On-Screen Display

- **Top center**: Posture classification label (green = Good, red = Bad)
- **Left side**: Angle values (Neck, Shoulder, Torso) -- red if exceeding threshold
- **Top right**: FPS counter
- **Bottom left**: Session timer (HH:MM:SS)
- **Center**: "PAUSED" indicator when analysis is paused

---

## Configuration

Edit `config.json` in the project root to customize posture thresholds:

```json
{
    "neck_threshold": 25,
    "shoulder_threshold": 10,
    "torso_threshold": 20,
    "min_visibility_confidence": 0.5,
    "camera_index": 0
}
```

| Setting                    | Default | Description                                              |
|----------------------------|---------|----------------------------------------------------------|
| `neck_threshold`           | 25      | Maximum neck inclination angle (degrees) for good posture |
| `shoulder_threshold`       | 10      | Maximum shoulder alignment deviation (degrees)            |
| `torso_threshold`          | 20      | Maximum torso-hip angle from vertical (degrees)           |
| `min_visibility_confidence`| 0.5     | Minimum landmark visibility score (0-1) to classify       |
| `camera_index`             | 0       | Webcam device index (0 = default camera)                  |

If the config file is missing or contains invalid values, the application uses the defaults shown above.

---

## Session Summary

When you press `q` to quit, a summary is printed to the console:

```
==================================================
  SESSION SUMMARY
==================================================
  Duration:             00:15:32
  Good Posture Time:    00:11:08
  Bad Posture Time:     00:04:24
  Good Posture:         71.6%
  Bad Posture:          28.4%
──────────────────────────────────────────────────
  Avg Neck Angle:       18.3 deg
  Avg Shoulder Angle:   5.7 deg
  Avg Torso Angle:      12.1 deg
==================================================
```

---

## Project Structure

```
posture-analysis-system/
├── main.py                  # Application entry point
├── config.json              # Posture threshold configuration
├── requirements.txt         # Python dependencies
├── README.md                # This file
├── src/
│   ├── __init__.py          # Package exports
│   ├── config.py            # Config loader with validation
│   ├── video_capture.py     # Webcam capture and release
│   ├── pose_detector.py     # MediaPipe landmark detection
│   ├── posture_analyzer.py  # Angle calculation and classification
│   ├── session_manager.py   # Timer, statistics, and summary
│   └── display_manager.py   # Visual overlays and rendering
└── docs/
    ├── Lab_Project.md       # Project summary
    └── BRD.md               # Business Requirements Document
```

---

## Troubleshooting

### "No camera detected" or "not authorized to capture video"

**macOS:**

1. Go to **System Settings > Privacy & Security > Camera**.
2. Enable the toggle for your terminal app (Terminal, iTerm2, VS Code, etc.).
3. If your terminal app does not appear in the list, run the app once so macOS registers it, then check again.
4. **Restart your terminal app** after granting permission.
5. If using **VS Code integrated terminal**, grant camera access to **Visual Studio Code** specifically.

**Windows:**

1. Go to **Settings > Privacy & Security > Camera**.
2. Make sure **Camera access** is turned **On**.
3. Ensure **"Let desktop apps access your camera"** is turned **On**.
4. If using an external USB webcam, check that drivers are installed.

**Both:**

- Ensure your webcam is not in use by another application (Zoom, Teams, etc.).
- Try a different camera index in `config.json` (e.g., `"camera_index": 1`).

### Low FPS or laggy video

- Close other applications using the camera.
- Ensure adequate lighting for better landmark detection.
- The system targets 15+ FPS on standard hardware.

### "No person detected" on screen

- Make sure your upper body (head, shoulders, torso) is visible to the camera.
- Sit 0.5-1.5 meters from the camera.
- Improve ambient lighting -- avoid backlighting.

### "Low Confidence -- Unable to Classify"

- This means the upper-body landmarks (ears, shoulders) are not detected with enough confidence.
- Improve lighting and ensure your face and shoulders are clearly visible.
- You can lower the threshold in `config.json`: set `"min_visibility_confidence"` to `0.3` or `0.1`.

### pip install fails with "externally-managed-environment" (macOS)

- You must use a virtual environment. Follow the macOS installation steps above.

### PowerShell execution policy error (Windows)

- Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- Then retry activating the virtual environment.

### ModuleNotFoundError when running

- Make sure the virtual environment is activated.
  - macOS: `source venv/bin/activate`
  - Windows CMD: `venv\Scripts\activate`
  - Windows PowerShell: `.\venv\Scripts\Activate.ps1`
- Re-run `pip install -r requirements.txt` inside the venv.

---

## Technology Stack

| Component        | Technology         |
|------------------|--------------------|
| Language         | Python 3.9+        |
| Video Processing | OpenCV 4.x         |
| Pose Detection   | MediaPipe Pose      |
| Math/Geometry    | NumPy               |
| Configuration    | JSON (stdlib)       |

---

## Privacy

This application does **not** record, store, or transmit any video data. All processing happens in memory and no frames are written to disk.
