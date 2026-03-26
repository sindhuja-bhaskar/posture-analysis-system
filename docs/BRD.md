# Business Requirements Document: Real-Time Posture Analysis System

| Field               | Value                                      |
|---------------------|--------------------------------------------|
| Document Version    | 1.0                                        |
| Date                | 2026-03-25                                 |
| Status              | Draft                                      |
| Author              | Business Requirements Analyst              |
| Classification      | Internal                                   |

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Project Objectives](#2-project-objectives)
3. [Business Need / Problem Statement](#3-business-need--problem-statement)
4. [Scope](#4-scope)
5. [Stakeholders](#5-stakeholders)
6. [Functional Requirements](#6-functional-requirements)
7. [Non-Functional Requirements](#7-non-functional-requirements)
8. [User Stories with Acceptance Criteria](#8-user-stories-with-acceptance-criteria)
9. [System Overview / Architecture](#9-system-overview--architecture)
10. [Assumptions and Constraints](#10-assumptions-and-constraints)
11. [Dependencies](#11-dependencies)
12. [Success Criteria / KPIs](#12-success-criteria--kpis)
13. [Risks and Mitigations](#13-risks-and-mitigations)
14. [Glossary](#14-glossary)

---

## 1. Executive Summary

This document defines the business requirements for a **Real-Time Posture Analysis System** -- a desktop application that uses a standard webcam and computer vision to detect, classify, and provide feedback on a user's sitting or standing posture. The system leverages OpenCV for video capture and processing, and MediaPipe Pose for human body landmark detection. By calculating joint angles derived from key anatomical points (neck, shoulders, hips, spine), the system classifies posture as "Good" or "Bad" and delivers immediate on-screen feedback.

The primary purpose is to promote healthy postural habits in academic, workplace, and personal environments. The system is designed as a modular, OOP-based Python application suitable for demonstration as a lab/capstone project, with a clear extension path toward fitness monitoring, rehabilitation support, and workplace ergonomics tooling.

This BRD provides the complete requirements baseline for technical estimation, architecture design, and implementation planning.

---

## 2. Project Objectives

| ID    | Objective                                                                                          | Measurable Target                                      |
|-------|----------------------------------------------------------------------------------------------------|--------------------------------------------------------|
| OBJ-1 | Detect human body landmarks in real time from a webcam feed                                       | Landmarks detected at >= 15 FPS on standard hardware   |
| OBJ-2 | Calculate body angles from detected landmarks to assess posture                                    | Angle calculations accurate within +/- 5 degrees       |
| OBJ-3 | Classify posture as "Good" or "Bad" based on configurable angle thresholds                        | Classification accuracy >= 85% against labeled dataset  |
| OBJ-4 | Provide real-time visual feedback to the user on posture quality                                   | Feedback latency <= 200ms from pose change              |
| OBJ-5 | Build a modular, extensible codebase using OOP principles                                          | Minimum 3 decoupled modules (capture, detection, analysis) |
| OBJ-6 | Enable users to monitor and improve their posture during extended sitting or standing sessions      | Users can run a session for >= 60 minutes continuously  |

---

## 3. Business Need / Problem Statement

### Problem

Prolonged poor posture during computer work, study sessions, and sedentary activities is a leading contributor to musculoskeletal disorders (MSDs), including chronic back pain, neck strain, and repetitive stress injuries. Most people are unaware of their posture deterioration until pain symptoms appear. Existing posture correction solutions fall into three categories, each with significant drawbacks:

1. **Wearable devices** -- Require purchase of specialized hardware; often uncomfortable for extended wear; battery-dependent.
2. **Manual self-monitoring** -- Unreliable; humans habituate and stop noticing slouching within minutes.
3. **Professional ergonomic assessments** -- Expensive, one-time, and do not provide continuous real-time monitoring.

### Opportunity

A software-only solution using a standard webcam (already present on most laptops and desktops) can provide continuous, real-time posture monitoring at zero additional hardware cost. This makes posture analysis accessible to students, office workers, and anyone with a computer.

### Business Value

- **For individuals**: Reduced risk of chronic pain; improved awareness of postural habits.
- **For academic institutions**: Demonstrates practical application of computer vision, OOP, and real-time systems.
- **For future extension**: Foundation for workplace wellness tools, physical therapy aids, and fitness coaching systems.

---

## 4. Scope

### 4.1 In-Scope

| ID       | Item                                                                                     |
|----------|------------------------------------------------------------------------------------------|
| SCOPE-01 | Real-time video capture from a single webcam                                             |
| SCOPE-02 | Human body landmark detection using MediaPipe Pose                                       |
| SCOPE-03 | Calculation of body angles: neck inclination, shoulder alignment, torso/hip angle         |
| SCOPE-04 | Posture classification into two categories: "Good Posture" and "Bad Posture"             |
| SCOPE-05 | Real-time on-screen visual overlay showing detected landmarks and posture classification  |
| SCOPE-06 | Color-coded feedback (e.g., green for good, red for bad) on the video feed               |
| SCOPE-07 | Configurable angle thresholds for posture classification                                 |
| SCOPE-08 | Session timer displaying elapsed monitoring time                                         |
| SCOPE-09 | Summary statistics at session end (total time, percentage in good/bad posture)            |
| SCOPE-10 | Modular OOP architecture with separated concerns (capture, detection, analysis, display)  |
| SCOPE-11 | Graceful start/stop of monitoring sessions via keyboard controls                         |
| SCOPE-12 | Documentation: README, setup instructions, and architecture overview                     |

### 4.2 Out of Scope

| ID       | Item                                                                                     | Rationale                                        |
|----------|------------------------------------------------------------------------------------------|--------------------------------------------------|
| OOS-01   | Multi-camera or depth-camera (e.g., Intel RealSense) support                             | Lab scope; single webcam is the target           |
| OOS-02   | Mobile or web application interface                                                      | Desktop-only for initial version                 |
| OOS-03   | Cloud-based processing or remote video streaming                                         | All processing is local                          |
| OOS-04   | Multi-person posture detection simultaneously                                            | Single-user system                               |
| OOS-05   | Historical data persistence or database storage                                          | Session-only data; no long-term storage          |
| OOS-06   | Integration with external health or fitness platforms                                    | Out of scope for lab project                     |
| OOS-07   | Audio/haptic feedback mechanisms                                                         | Visual feedback only                             |
| OOS-08   | Custom ML model training for posture classification                                      | Uses MediaPipe pre-trained model + angle rules   |
| OOS-09   | HIPAA or medical-grade compliance                                                        | Non-medical tool; informational only             |
| OOS-10   | User authentication or multi-user profiles                                               | Single-user desktop application                  |

---

## 5. Stakeholders

| Role                     | Name / Group         | Interest                                                         | Influence |
|--------------------------|----------------------|------------------------------------------------------------------|-----------|
| Project Sponsor          | Course Instructor    | Project meets academic requirements and demonstrates competency  | High      |
| Primary User             | Student / Developer  | Monitors their own posture during computer use                   | High      |
| Development Team         | Lab Project Team     | Builds and delivers the system                                   | High      |
| Evaluator                | Academic Reviewer    | Assesses code quality, design patterns, and functionality        | Medium    |
| Future Extensibility User| Workplace / Fitness  | Potential downstream consumers if the project is extended         | Low       |

---

## 6. Functional Requirements

### FR-001: Video Capture

**Description**: The system shall capture live video frames from the user's default webcam in real time.

| Attribute          | Detail                                                              |
|--------------------|---------------------------------------------------------------------|
| Priority           | Must-Have                                                           |
| Source             | OBJ-1                                                               |
| Input              | Webcam hardware device                                              |
| Output             | Continuous stream of video frames (BGR color space)                 |
| Business Rule      | If no webcam is detected, the system shall display an error message and terminate gracefully. |

**Acceptance Criteria**:
- AC-001.1: Given a connected webcam, when the application starts, then video frames are captured at the webcam's native resolution.
- AC-001.2: Given no webcam is connected, when the application starts, then an error message "No camera detected. Please connect a webcam and restart." is displayed and the application exits with a non-zero code.
- AC-001.3: Given the webcam is active, when frames are being captured, then the frame rate is at least 15 FPS.

---

### FR-002: Body Landmark Detection

**Description**: The system shall detect human body landmarks (pose keypoints) in each video frame using MediaPipe Pose.

| Attribute          | Detail                                                              |
|--------------------|---------------------------------------------------------------------|
| Priority           | Must-Have                                                           |
| Source             | OBJ-1                                                               |
| Input              | Video frame (BGR image)                                             |
| Output             | Set of 33 pose landmarks with (x, y, z) coordinates and visibility confidence scores |
| Business Rule      | If no person is detected in the frame, the system shall display a "No person detected" indicator on screen. |

**Acceptance Criteria**:
- AC-002.1: Given a video frame containing a visible person, when the frame is processed, then at least the following landmarks are detected: left shoulder, right shoulder, left hip, right hip, left ear, right ear, nose.
- AC-002.2: Given a video frame with no person visible, when the frame is processed, then the system displays "No person detected" on the video overlay.
- AC-002.3: Given a detected pose, when landmarks are returned, then each landmark includes x, y coordinates normalized to [0, 1] and a visibility confidence score.

---

### FR-003: Angle Calculation

**Description**: The system shall calculate relevant body angles from detected landmarks to quantify posture alignment.

| Attribute          | Detail                                                              |
|--------------------|---------------------------------------------------------------------|
| Priority           | Must-Have                                                           |
| Source             | OBJ-2                                                               |
| Input              | Pose landmark coordinates                                           |
| Output             | Calculated angles in degrees: neck inclination angle, shoulder alignment angle, torso-hip angle |
| Business Rule      | Angles are computed using the three-point angle formula (law of cosines or atan2-based vector method). |

**Acceptance Criteria**:
- AC-003.1: Given detected landmarks for the neck (ear-shoulder vector) and vertical reference, when angles are calculated, then the neck inclination angle is returned in degrees (0-180).
- AC-003.2: Given detected left and right shoulder landmarks, when the shoulder alignment angle is calculated, then the deviation from horizontal is returned in degrees.
- AC-003.3: Given detected shoulder and hip landmarks, when the torso angle is calculated, then the torso inclination from vertical is returned in degrees.
- AC-003.4: Given a known test pose with pre-measured angles, when the system calculates angles, then the results are accurate within +/- 5 degrees of the expected values.

---

### FR-004: Posture Classification

**Description**: The system shall classify the user's current posture as "Good Posture" or "Bad Posture" based on the calculated angles and configurable thresholds.

| Attribute          | Detail                                                              |
|--------------------|---------------------------------------------------------------------|
| Priority           | Must-Have                                                           |
| Source             | OBJ-3                                                               |
| Input              | Calculated body angles                                               |
| Output             | Classification label: "Good Posture" or "Bad Posture"              |
| Business Rule      | Posture is "Good" if ALL measured angles fall within their respective threshold ranges. Posture is "Bad" if ANY angle exceeds its threshold. |

**Default Thresholds** (configurable):

| Angle                    | Good Posture Range     | Bad Posture Condition        |
|--------------------------|------------------------|------------------------------|
| Neck Inclination         | 0 - 25 degrees         | > 25 degrees                 |
| Shoulder Alignment       | 0 - 10 degrees         | > 10 degrees deviation       |
| Torso-Hip Angle          | 0 - 20 degrees         | > 20 degrees from vertical   |

**Acceptance Criteria**:
- AC-004.1: Given all calculated angles are within the "Good" threshold, when classification runs, then the output is "Good Posture".
- AC-004.2: Given the neck inclination angle exceeds 25 degrees (default threshold), when classification runs, then the output is "Bad Posture".
- AC-004.3: Given custom thresholds are configured (e.g., neck threshold set to 30 degrees), when classification runs, then the system uses the custom threshold values.
- AC-004.4: Given landmark detection confidence is below a minimum threshold (e.g., visibility < 0.5), when classification runs, then the system outputs "Low Confidence -- Unable to Classify" instead of a posture label.

---

### FR-005: Real-Time Visual Feedback

**Description**: The system shall overlay posture feedback on the live video feed in real time.

| Attribute          | Detail                                                              |
|--------------------|---------------------------------------------------------------------|
| Priority           | Must-Have                                                           |
| Source             | OBJ-4                                                               |
| Input              | Video frame, landmark positions, classification result              |
| Output             | Annotated video frame displayed to the user                        |

**Acceptance Criteria**:
- AC-005.1: Given a "Good Posture" classification, when the frame is displayed, then the posture label is shown in green text on the video overlay.
- AC-005.2: Given a "Bad Posture" classification, when the frame is displayed, then the posture label is shown in red text on the video overlay.
- AC-005.3: Given detected landmarks, when the frame is displayed, then landmark points and skeletal connections are drawn on the user's body in the video.
- AC-005.4: Given the system is running, when each frame is rendered, then the calculated angle values (neck, shoulder, torso) are displayed numerically on the overlay.
- AC-005.5: Given a posture change occurs, when the next frame is rendered, then the updated classification is visible within 200 milliseconds of the pose change.

---

### FR-006: Session Management

**Description**: The system shall support starting, running, and stopping a posture monitoring session.

| Attribute          | Detail                                                              |
|--------------------|---------------------------------------------------------------------|
| Priority           | Must-Have                                                           |
| Source             | OBJ-6                                                               |
| Input              | User keyboard input                                                 |
| Output             | Session state transitions (idle -> running -> stopped)              |

**Acceptance Criteria**:
- AC-006.1: Given the application is launched, when the video feed initializes successfully, then the monitoring session starts automatically.
- AC-006.2: Given a session is active, when the user presses the 'q' key, then the session stops, the webcam is released, and all OpenCV windows are closed.
- AC-006.3: Given a session is active, when the video feed is displayed, then a session timer (elapsed time in HH:MM:SS) is shown on the overlay.
- AC-006.4: Given a session is active, when the user presses the 'p' key, then the session is paused (frame capture continues but analysis and classification halt). Pressing 'p' again resumes.

---

### FR-007: Session Summary

**Description**: The system shall display a summary of posture statistics when a session ends.

| Attribute          | Detail                                                              |
|--------------------|---------------------------------------------------------------------|
| Priority           | Should-Have                                                         |
| Source             | OBJ-6                                                               |
| Input              | Accumulated session data                                            |
| Output             | Summary printed to console or displayed in a summary window        |

**Acceptance Criteria**:
- AC-007.1: Given a session has ended, when the summary is generated, then it includes: total session duration, total time in good posture, total time in bad posture, and percentage of time in good posture.
- AC-007.2: Given a session lasted 10 minutes with 7 minutes good posture and 3 minutes bad posture, when the summary displays, then it shows "Good Posture: 70.0% | Bad Posture: 30.0%".
- AC-007.3: Given a session has ended, when the summary is generated, then the average neck angle, shoulder angle, and torso angle for the session are included.

---

### FR-008: Threshold Configuration

**Description**: The system shall allow posture classification thresholds to be configured without code changes.

| Attribute          | Detail                                                              |
|--------------------|---------------------------------------------------------------------|
| Priority           | Should-Have                                                         |
| Source             | OBJ-3                                                               |
| Input              | Configuration file (e.g., JSON or YAML) or command-line arguments  |
| Output             | Updated threshold values used by the classification engine         |

**Acceptance Criteria**:
- AC-008.1: Given a configuration file exists at a known path, when the application starts, then threshold values are loaded from the file.
- AC-008.2: Given no configuration file exists, when the application starts, then default threshold values are used (as defined in FR-004).
- AC-008.3: Given a configuration file with an invalid value (e.g., negative angle), when the application starts, then a validation error is logged and default values are used.

---

### FR-009: Landmark Visualization

**Description**: The system shall draw detected body landmarks and skeletal connections on the video feed.

| Attribute          | Detail                                                              |
|--------------------|---------------------------------------------------------------------|
| Priority           | Must-Have                                                           |
| Source             | OBJ-1, OBJ-4                                                       |
| Input              | Detected pose landmarks                                             |
| Output             | Visual overlay of points and lines on the video frame              |

**Acceptance Criteria**:
- AC-009.1: Given landmarks are detected, when the frame is rendered, then each key landmark (shoulders, hips, ears, nose) is drawn as a circle on the video.
- AC-009.2: Given landmarks are detected, when the frame is rendered, then skeletal connections (e.g., shoulder-to-hip, shoulder-to-ear) are drawn as lines between landmarks.
- AC-009.3: Given a "Bad Posture" classification, when the frame is rendered, then the skeletal lines for the offending angle are highlighted in red.

---

## 7. Non-Functional Requirements

### NFR-001: Performance

| Attribute          | Detail                                                              |
|--------------------|---------------------------------------------------------------------|
| Requirement        | The system shall process and display annotated frames at a minimum of 15 frames per second on the target hardware. |
| Rationale          | Real-time feedback requires smooth video rendering; below 15 FPS the user perceives noticeable lag. |
| Measurement        | Average FPS measured over a 60-second session using an on-screen FPS counter. |

---

### NFR-002: Latency

| Attribute          | Detail                                                              |
|--------------------|---------------------------------------------------------------------|
| Requirement        | End-to-end latency from frame capture to annotated display shall not exceed 200 milliseconds. |
| Rationale          | Users must see posture feedback that corresponds to their current position, not a delayed state. |
| Measurement        | Timestamp difference between frame capture and frame render, logged and averaged over 100 frames. |

---

### NFR-003: Resource Utilization

| Attribute          | Detail                                                              |
|--------------------|---------------------------------------------------------------------|
| Requirement        | The system shall consume no more than 50% of a single CPU core and no more than 500 MB of RAM during operation. |
| Rationale          | The system runs alongside other applications (browser, IDE, etc.); it must not degrade overall system performance. |
| Measurement        | CPU and memory usage monitored via system profiling tools during a 30-minute session. |

---

### NFR-004: Reliability

| Attribute          | Detail                                                              |
|--------------------|---------------------------------------------------------------------|
| Requirement        | The system shall run continuously for at least 60 minutes without crashes, memory leaks, or frame rate degradation exceeding 20%. |
| Rationale          | Typical work or study sessions last 1-2 hours; the system must be stable for the duration. |
| Measurement        | Stability test: run 3 consecutive 60-minute sessions; all must complete without error. |

---

### NFR-005: Usability

| Attribute          | Detail                                                              |
|--------------------|---------------------------------------------------------------------|
| Requirement        | The system shall be operable with no more than 2 user interactions: launch the application and press 'q' to quit. |
| Rationale          | The target user is not necessarily technical; the system should be zero-configuration for basic use. |
| Measurement        | A new user can start and stop a session within 30 seconds without documentation. |

---

### NFR-006: Portability

| Attribute          | Detail                                                              |
|--------------------|---------------------------------------------------------------------|
| Requirement        | The system shall run on Windows 10+, macOS 12+, and Ubuntu 20.04+ with Python 3.9+ installed. |
| Rationale          | Lab environments use mixed operating systems; cross-platform support is necessary. |
| Measurement        | Successful execution of all functional requirements on each target OS. |

---

### NFR-007: Maintainability

| Attribute          | Detail                                                              |
|--------------------|---------------------------------------------------------------------|
| Requirement        | The codebase shall follow OOP principles with a minimum of 3 distinct classes (VideoCapture, PoseDetector, PostureAnalyzer) and separation of concerns. |
| Rationale          | Academic requirement; also enables future extension and independent testing. |
| Measurement        | Code review confirms class separation; each class can be unit-tested independently. |

---

### NFR-008: Privacy

| Attribute          | Detail                                                              |
|--------------------|---------------------------------------------------------------------|
| Requirement        | The system shall not record, store, or transmit any video data. All processing occurs in-memory and no frames are written to disk. |
| Rationale          | User privacy; webcam data is sensitive and must not persist beyond the active session. |
| Measurement        | Code review and filesystem audit confirm no file write operations for video/image data. |

---

## 8. User Stories with Acceptance Criteria

### US-01: Start Posture Monitoring

```
As a computer user,
I want to launch the posture analysis application and have it immediately begin monitoring my posture,
So that I can receive feedback without manual configuration.
```

**Acceptance Criteria**:

- Given I have a webcam connected and Python dependencies installed, when I run the application (e.g., `python main.py`), then the video feed opens in a window and posture analysis begins within 3 seconds.
- Given I do not have a webcam connected, when I run the application, then I see an error message and the application exits cleanly.

**Priority**: Must-Have | **Estimated Effort**: Small

---

### US-02: See My Posture Classification in Real Time

```
As a user sitting at my desk,
I want to see whether my current posture is "Good" or "Bad" overlaid on the video feed,
So that I can immediately correct my posture when it deteriorates.
```

**Acceptance Criteria**:

- Given I am sitting with a straight back and my face is visible to the camera, when the system processes the frame, then the label "Good Posture" is displayed in green text.
- Given I am slouching forward with my neck at a steep angle, when the system processes the frame, then the label "Bad Posture" is displayed in red text.
- Given I change from good posture to bad posture, when the next frame is rendered, then the label updates within 200ms.

**Priority**: Must-Have | **Estimated Effort**: Medium

---

### US-03: View Skeletal Overlay

```
As a user,
I want to see the detected body landmarks and skeletal connections drawn on the video feed,
So that I can understand which body points the system is tracking and verify its accuracy.
```

**Acceptance Criteria**:

- Given my upper body is visible to the camera, when pose detection succeeds, then circles are drawn at each detected landmark and lines connect related landmarks.
- Given I move my shoulders, when the next frame renders, then the skeletal overlay tracks my movement smoothly.

**Priority**: Must-Have | **Estimated Effort**: Small

---

### US-04: View Angle Measurements

```
As a user concerned about specific posture metrics,
I want to see the numerical angle values (neck, shoulders, torso) displayed on screen,
So that I can track the specific measurements contributing to my posture score.
```

**Acceptance Criteria**:

- Given pose detection is active, when a frame is displayed, then the current neck angle, shoulder alignment angle, and torso angle are displayed as numerical values (e.g., "Neck: 15 deg").
- Given an angle exceeds the "Bad Posture" threshold, when displayed, then that angle value is rendered in red text to indicate the offending metric.

**Priority**: Should-Have | **Estimated Effort**: Small

---

### US-05: Stop Monitoring and See Summary

```
As a user finishing a work session,
I want to press 'q' to stop monitoring and see a summary of my posture during the session,
So that I can understand my overall posture quality for the session.
```

**Acceptance Criteria**:

- Given a monitoring session is active, when I press the 'q' key, then the video window closes, the webcam is released, and a session summary is printed to the console.
- Given my session lasted 30 minutes with 24 minutes of good posture, when the summary displays, then it shows total duration (00:30:00), good posture time (00:24:00), bad posture time (00:06:00), and good posture percentage (80.0%).

**Priority**: Should-Have | **Estimated Effort**: Medium

---

### US-06: Pause and Resume Monitoring

```
As a user who needs to step away briefly,
I want to pause the posture analysis without closing the application,
So that my session statistics are not affected by periods when I am away from the desk.
```

**Acceptance Criteria**:

- Given a session is active, when I press 'p', then analysis pauses, the overlay shows "Paused", and posture statistics stop accumulating.
- Given the session is paused, when I press 'p' again, then analysis resumes and the "Paused" indicator disappears.

**Priority**: Could-Have | **Estimated Effort**: Small

---

### US-07: Customize Posture Thresholds

```
As a user with specific posture needs (e.g., physical therapy),
I want to adjust the angle thresholds that define good vs. bad posture,
So that the system is calibrated to my personal ergonomic requirements.
```

**Acceptance Criteria**:

- Given I create a config file (e.g., `config.json`) with custom thresholds, when I launch the application, then the system uses my custom values.
- Given my config file has an invalid entry (e.g., `"neck_threshold": -10`), when the application starts, then a warning is logged, the invalid value is ignored, and the default value is used for that threshold.

**Priority**: Should-Have | **Estimated Effort**: Small

---

### US-08: Handle No Person in Frame

```
As a user who may move in and out of camera view,
I want the system to gracefully indicate when it cannot detect a person,
So that I am not confused by stale or incorrect posture readings.
```

**Acceptance Criteria**:

- Given no person is visible in the camera frame, when the system processes the frame, then the overlay displays "No person detected" and no posture classification is shown.
- Given a person re-enters the frame after being absent, when landmarks are detected again, then posture classification resumes within the next frame cycle.

**Priority**: Must-Have | **Estimated Effort**: Small

---

## 9. System Overview / Architecture

### 9.1 High-Level Architecture

```
+-------------------+     +--------------------+     +---------------------+
|                   |     |                    |     |                     |
|   VideoCapture    |---->|   PoseDetector     |---->|  PostureAnalyzer    |
|   Module          |     |   Module           |     |  Module             |
|                   |     |                    |     |                     |
| - Webcam init     |     | - MediaPipe Pose   |     | - Angle calculator  |
| - Frame capture   |     | - Landmark extract |     | - Threshold engine  |
| - Frame release   |     | - Confidence check |     | - Classification    |
+-------------------+     +--------------------+     +---------------------+
                                                              |
                                                              v
                          +--------------------+     +---------------------+
                          |                    |     |                     |
                          |   DisplayManager   |<----|  SessionManager     |
                          |   Module           |     |  Module             |
                          |                    |     |                     |
                          | - Overlay render   |     | - Timer             |
                          | - Color coding     |     | - Stats accumulator |
                          | - FPS counter      |     | - Summary generator |
                          +--------------------+     +---------------------+
```

### 9.2 Module Responsibilities

| Module             | Responsibility                                                  | Key Class(es)         |
|--------------------|-----------------------------------------------------------------|-----------------------|
| VideoCapture       | Initialize webcam, capture frames, release resources            | `VideoCapture`        |
| PoseDetector       | Process frames through MediaPipe, extract landmarks, check confidence | `PoseDetector`   |
| PostureAnalyzer    | Calculate angles, apply thresholds, classify posture            | `PostureAnalyzer`     |
| DisplayManager     | Render overlays (landmarks, skeleton, labels, angles, timer)    | `DisplayManager`      |
| SessionManager     | Track session time, accumulate posture statistics, generate summary | `SessionManager`  |

### 9.3 Technology Stack

| Component          | Technology                                                      |
|--------------------|-----------------------------------------------------------------|
| Language           | Python 3.9+                                                    |
| Video Processing   | OpenCV (cv2) 4.x                                               |
| Pose Detection     | MediaPipe Pose (google-mediapipe)                               |
| Math/Geometry      | NumPy                                                          |
| Configuration      | JSON (standard library) or PyYAML                               |
| Packaging          | pip + requirements.txt                                          |

### 9.4 Data Flow

1. `VideoCapture` reads a frame from the webcam.
2. The frame is passed to `PoseDetector`, which runs MediaPipe Pose inference and returns landmark coordinates with confidence scores.
3. If landmarks are detected with sufficient confidence, `PostureAnalyzer` calculates angles and classifies posture.
4. `SessionManager` records the classification result and updates running statistics.
5. `DisplayManager` composites the annotated frame (landmarks, skeleton, labels, angles, timer) and renders it to an OpenCV window.
6. The loop repeats until the user presses 'q'.
7. On exit, `SessionManager` generates and outputs the session summary.

---

## 10. Assumptions and Constraints

### 10.1 Assumptions

| ID     | Assumption                                                                                        |
|--------|---------------------------------------------------------------------------------------------------|
| ASM-01 | The user has a functioning webcam capable of at least 640x480 resolution at 15+ FPS.              |
| ASM-02 | The user is the only person visible in the camera frame during a session.                         |
| ASM-03 | The user's upper body (head, shoulders, torso) is visible to the camera during use.               |
| ASM-04 | Ambient lighting is sufficient for the camera to capture a clear image of the user.               |
| ASM-05 | Python 3.9+ and pip are pre-installed on the user's machine.                                     |
| ASM-06 | The system is used in a seated or standing desk scenario (not during exercise or movement).       |
| ASM-07 | MediaPipe Pose provides sufficiently accurate landmark detection for posture assessment at typical webcam distances (0.5-1.5 meters). |
| ASM-08 | A two-class classification (Good/Bad) is sufficient for the initial version.                      |

### 10.2 Constraints

| ID     | Constraint                                                                                        |
|--------|---------------------------------------------------------------------------------------------------|
| CON-01 | **Academic scope**: This is a lab/capstone project with a fixed delivery timeline.                |
| CON-02 | **No custom ML training**: The system uses MediaPipe's pre-trained model only; no fine-tuning.   |
| CON-03 | **Single user**: Only one person can be analyzed at a time.                                       |
| CON-04 | **Local processing only**: No cloud APIs or network calls; the system must work fully offline.    |
| CON-05 | **No data persistence**: No video recording, no database, no file-based session history.         |
| CON-06 | **Desktop only**: No web or mobile interface; OpenCV window is the sole UI.                      |
| CON-07 | **Budget**: Zero cost -- all tools, libraries, and dependencies must be free/open-source.        |

---

## 11. Dependencies

### 11.1 Software Dependencies

| Dependency           | Version       | Purpose                            | License       |
|----------------------|---------------|------------------------------------|---------------|
| Python               | >= 3.9        | Runtime environment                | PSF           |
| OpenCV (opencv-python)| >= 4.5       | Video capture and image processing | Apache 2.0    |
| MediaPipe            | >= 0.10       | Pose landmark detection            | Apache 2.0    |
| NumPy                | >= 1.21       | Mathematical computations          | BSD           |

### 11.2 Hardware Dependencies

| Dependency           | Specification                                                     |
|----------------------|-------------------------------------------------------------------|
| Webcam               | USB or integrated; minimum 640x480 @ 15 FPS; UVC-compatible      |
| CPU                  | Minimum dual-core, 2.0 GHz (Intel i5 / AMD Ryzen 3 equivalent)  |
| RAM                  | Minimum 4 GB (500 MB available for the application)              |
| Display              | Minimum 1280x720 to view the video overlay window                |

### 11.3 External Dependencies

| Dependency           | Detail                                                            |
|----------------------|-------------------------------------------------------------------|
| MediaPipe Model      | Pre-trained pose estimation model bundled with the MediaPipe package; no network required at runtime |
| OS Camera Drivers    | The operating system must provide a working camera driver recognized by OpenCV |

---

## 12. Success Criteria / KPIs

| ID     | KPI                                           | Target                              | Measurement Method                                    |
|--------|-----------------------------------------------|--------------------------------------|-------------------------------------------------------|
| KPI-01 | Frame Processing Rate                         | >= 15 FPS                           | On-screen FPS counter averaged over 60 seconds        |
| KPI-02 | Posture Classification Accuracy               | >= 85% against labeled test poses   | Manual testing with 20 pre-defined poses (10 good, 10 bad) |
| KPI-03 | End-to-End Feedback Latency                   | <= 200 ms                           | Timestamped logs for frame capture vs. display render  |
| KPI-04 | Session Stability                             | 60 minutes without crash            | 3 consecutive 60-minute test runs                     |
| KPI-05 | Memory Stability                              | < 10% memory growth over 60 minutes | Memory profiling at T=0, T=30m, T=60m                 |
| KPI-06 | Code Modularity                               | >= 3 independent, testable classes  | Code review / static analysis                         |
| KPI-07 | Cross-Platform Compatibility                  | Runs on Windows, macOS, Linux       | Execution test on each OS                             |
| KPI-08 | Session Summary Accuracy                      | Summary percentages match manual count within 1% | Compare summary output to manually counted frame classifications |
| KPI-09 | Zero Data Persistence                         | No video/image files written        | Filesystem audit after a 30-minute session            |
| KPI-10 | User Satisfaction (Subjective)                | User finds feedback helpful         | Informal usability test with 3 users                  |

---

## 13. Risks and Mitigations

| ID     | Risk                                              | Likelihood | Impact   | Mitigation Strategy                                                                                         |
|--------|---------------------------------------------------|------------|----------|-------------------------------------------------------------------------------------------------------------|
| RSK-01 | **Low FPS on older hardware**: MediaPipe inference may exceed frame budget on low-end CPUs. | Medium | High | Use MediaPipe's "lite" model complexity setting; reduce input resolution to 480p; provide FPS on overlay so users can assess performance. |
| RSK-02 | **Poor lighting degrades landmark detection**: Dim or backlit environments cause MediaPipe to miss landmarks. | High | Medium | Document recommended lighting conditions in README; display confidence scores and "Low Confidence" warnings on overlay. |
| RSK-03 | **Angle thresholds are not universally valid**: Different body types, chair heights, and camera angles affect what constitutes "good" posture. | High | Medium | Make thresholds configurable (FR-008); document that defaults are guidelines, not medical advice; consider adding a calibration step in future. |
| RSK-04 | **Single-person assumption violated**: If multiple people appear in the frame, MediaPipe may detect the wrong person. | Medium | Medium | Document single-user requirement; MediaPipe typically returns the most prominent person; add a check that warns if multiple detections are suspected. |
| RSK-05 | **Camera permission denied by OS**: Modern OS versions require explicit camera permission grants. | Medium | High | Detect permission errors distinctly from "no camera" errors; provide OS-specific troubleshooting in README. |
| RSK-06 | **Dependency version conflicts**: OpenCV and MediaPipe may have conflicting NumPy version requirements. | Low | Medium | Pin all dependency versions in requirements.txt; test installation on a clean virtual environment before delivery. |
| RSK-07 | **Scope creep into advanced features**: Temptation to add exercise tracking, ML-based classification, or UI frameworks. | Medium | Medium | Strict adherence to this BRD's in-scope/out-of-scope boundaries; defer enhancements to a documented future roadmap. |
| RSK-08 | **Privacy concerns from webcam usage**: Users may be uncomfortable with a webcam-based application. | Low | Low | Enforce NFR-008 (no data persistence); clearly state in README that no video is recorded or transmitted. |

---

## 14. Glossary

| Term                     | Definition                                                                                                     |
|--------------------------|----------------------------------------------------------------------------------------------------------------|
| **BGR**                  | Blue-Green-Red; the default color channel ordering used by OpenCV for image representation.                   |
| **FPS**                  | Frames Per Second; the number of video frames captured and processed per second.                              |
| **Landmark**             | A specific anatomical point on the body (e.g., left shoulder, right hip) detected by the pose estimation model. |
| **MediaPipe Pose**       | A machine learning pipeline by Google that detects 33 body landmarks from a single RGB image in real time.     |
| **Neck Inclination**     | The angle between the ear-shoulder line and the vertical axis; measures forward head posture.                  |
| **OpenCV**               | Open Source Computer Vision Library; provides functions for real-time image and video processing.              |
| **OOP**                  | Object-Oriented Programming; a paradigm organizing code into classes and objects with encapsulation, inheritance, and polymorphism. |
| **Pose Estimation**      | The computer vision task of detecting the position and orientation of a person's body from an image or video.  |
| **Shoulder Alignment**   | The angular deviation of the line connecting left and right shoulders from the horizontal plane.               |
| **Skeleton / Skeletal Overlay** | A visual representation of the detected body landmarks connected by lines, drawn on the video frame.    |
| **Threshold**            | A configurable angle value that defines the boundary between "Good Posture" and "Bad Posture" classification. |
| **Torso-Hip Angle**      | The angle of the torso (shoulder-to-hip line) relative to the vertical axis; measures slouching or leaning.    |
| **UVC**                  | USB Video Class; a standard protocol for USB webcams that allows them to work without vendor-specific drivers. |
| **Visibility Confidence**| A score (0 to 1) from MediaPipe indicating how confident the model is that a landmark is visible and correctly located. |

---

## Appendix A: Requirement Traceability Matrix

| Requirement | Objective(s) | User Story(ies) | Priority   |
|-------------|--------------|-----------------|------------|
| FR-001      | OBJ-1        | US-01           | Must-Have  |
| FR-002      | OBJ-1        | US-01, US-03    | Must-Have  |
| FR-003      | OBJ-2        | US-02, US-04    | Must-Have  |
| FR-004      | OBJ-3        | US-02, US-07    | Must-Have  |
| FR-005      | OBJ-4        | US-02, US-03    | Must-Have  |
| FR-006      | OBJ-6        | US-01, US-05, US-06 | Must-Have |
| FR-007      | OBJ-6        | US-05           | Should-Have|
| FR-008      | OBJ-3        | US-07           | Should-Have|
| FR-009      | OBJ-1, OBJ-4 | US-03          | Must-Have  |
| NFR-001     | OBJ-1        | --              | Must-Have  |
| NFR-002     | OBJ-4        | --              | Must-Have  |
| NFR-003     | --            | --              | Must-Have  |
| NFR-004     | OBJ-6        | --              | Must-Have  |
| NFR-005     | --            | US-01           | Must-Have  |
| NFR-006     | --            | --              | Should-Have|
| NFR-007     | OBJ-5        | --              | Must-Have  |
| NFR-008     | --            | --              | Must-Have  |

---

## Appendix B: Open Questions

| ID    | Question                                                                                           | Owner            | Due Date   |
|-------|----------------------------------------------------------------------------------------------------|------------------|------------|
| OQ-01 | Should the system support a "calibration" step where the user sits in ideal posture to personalize thresholds? | Project Team | TBD |
| OQ-02 | What is the minimum acceptable landmark visibility confidence score for classification? (Proposed: 0.5) | Project Team | TBD |
| OQ-03 | Should the session summary be written to a text file in addition to console output?                | Project Sponsor  | TBD        |
| OQ-04 | Is there a preferred camera resolution to target (e.g., 640x480 vs. 1280x720)?                    | Project Team     | TBD        |
| OQ-05 | Should the system emit an audible alert when bad posture is detected, or is visual-only sufficient? | Project Sponsor | TBD        |
| OQ-06 | What is the project delivery deadline?                                                              | Project Sponsor  | TBD        |
| OQ-07 | Are there specific evaluation rubric criteria that should be reflected in the architecture (e.g., minimum number of design patterns)? | Project Sponsor | TBD |

---

*End of Document*
