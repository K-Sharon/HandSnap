# HandSnap

**HandSnap** is a gesture-controlled screenshot capture system that lets you take screenshots using your webcam and hand gestures. When you close your fist in front of the camera, it captures your desktop screen and displays the screenshots in a clean, downloadable HTML gallery that can be opened directly from your mobile phone or desktop browser—without needing to run a server.

---

## Features

- Gesture-based screenshot capture using a webcam  
- Automatically saves screenshots with timestamps  
- Generates a responsive HTML viewer (`viewer.html`) for mobile and desktop access  
- Displays the latest screenshot by default with an option to view older ones  
- No server required — open the HTML file directly in any browser  

---

## Technologies Used

- **Python** – Core programming language  
- **OpenCV** – For webcam capture and video processing  
- **MediaPipe** – For real-time hand gesture recognition  
- **PyAutoGUI** – For desktop screenshot functionality  
- **HTML/CSS** – For building the screenshot viewer interface  

---

## How It Works

1. Run the Python script (`hand_gesture_screenshot.py`)  
2. Show your hand in front of the webcam  
3. Close your fist to capture a screenshot  
4. The captured image is saved in the `screenshots/` folder  
5. The HTML file (`viewer.html`) is updated automatically with the latest screenshot  
6. Open `viewer.html` in any browser (on PC or phone) to view or download the screenshots  

---
