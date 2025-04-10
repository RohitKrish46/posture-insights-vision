# 🧘‍♂️posture-insights-vision 

> Real-time exercise form correction using YOLOv8 pose estimation — your personal AI fitness assistant.

## 🚀 Overview

Posture Insights Vision is a computer vision-based system designed to provide real-time feedback on exercise posture and form. Leveraging YOLOv8's pose estimation, this project helps users self-correct during workouts by identifying improper alignment and joint angles, all through a simple web interface powered by Flask and OpenCV.

Whether you're doing push-ups, planks, or curls, this tool acts as your virtual personal trainer to ensure you're doing it right.

## 🧠 How It Works

![image](https://github.com/RohitKrish46/posture-insights-vision/assets/25106707/6b131930-6689-47d5-b977-507813de50d3)


1. **Web Interface Launch**: Users open a Flask-powered web interface and select an exercise.

2. **Webcam Activation**: The app activates the webcam to begin capturing live video.

3. **Pose Estimation**: Each frame is passed through YOLOv8's pose estimation model, detecting 17 key body joints in real-time.

4. **Heuristic Analysis**: Based on selected exercise, relevant joints are analyzed for:

    - Joint angles
    
    - Body alignment
    
    - Motion flow

5. **Real-Time Feedback**: If poor posture is detected, alerts are displayed on the UI instantly.

## 🎯Sample Output

![output](https://github.com/user-attachments/assets/6a959ea0-cee5-43b4-a9f7-62086ebdc9fa)  ![output_pushup](https://github.com/user-attachments/assets/bbdb582f-a8ed-408f-be4b-d805d79d8c7a)



## ⚙️ Features

- ✅ Real-time posture detection

- 🎯 Accurate joint tracking with YOLOv8

- 🧩 Modular exercise-specific heuristics

- 💻 Lightweight Flask app with webcam streaming

- 📈 Designed to work on local machines with webcam access


## 🧪 Supported Exercises & Heuristics

Each heuristic is designed using joint angle thresholds and motion trajectory tracking based on keypoints detected per frame:

1. **Plank** – Ensures shoulder, hip, and ankle are aligned in a straight line.

2. **Push-up** – Tracks elbow flexion and extension, back curvature, and wrist alignment.

3. **Bicep Curl** – Measures elbow joint angle to ensure full range of motion and controlled return.

## 🛠️ Getting Started


1. **Clone the Repository**: 
    ```
    git clone https://github.com/RohitKrish46/posture-insights-vision.git
    cd posture-insights-vision
    ```
2. **Create a Virtual Environment**:
   ```
   python -m venv env
   ```

3. **Activate the Virtual Environment**:
   
   - On Windows 
      ```
      env\Scripts\activate
      ```

   - On macOS and Linux
      ```
      source env/bin/activate
      ```

4. **Install Dependencies**: 
    ```
    pip install -r requirements.txt
    ```

5. **Download the YOLOV8 Model**:
    - Download the desired YOLOV8 model and store it under the 'models' folder.
    - You can download ultralytics models using:

      ```
      from ultralytics import YOLO
      model = YOLO('yolov8m-pose.pt')
      ```

6. **Launch the Flask App**: 
    ```
    flask run
    ```
   
8. **Open in Browser**:
   
   Navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000) to start using the app.


## 🧪 Playing with YOLOv8's Pose Estimation

YOLOv8's pose model is ideal for this use case due to:

- Single-pass detection of all keypoints

- High FPS for real-time inference

- Strong accuracy for joint localization

The model outputs coordinates for 17 joints, which are further processed using geometric and motion-based heuristics.

## Project Structure
```
posture-insights-vision/
│
├── app.py                   # Flask app entry point
├── models/                  # YOLOv8 model files
├── static/                  # CSS and JS files
├── templates/               # HTML templates
├── utils/
│   └── heuristics.py        # Heuristic functions for posture detection
├── requirements.txt
└── README.md
```

## 📌 Future Enhancements
1. 🏋️ Add more exercises (e.g., squats, lunges)

2. 📊 Add feedback history and performance metrics

3. 🤖 Integrate with fitness APIs for tracking

4. 📱 Port to mobile or desktop apps
