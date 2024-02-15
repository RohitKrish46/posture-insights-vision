# posture-insights-vision 

This project aims to assist anyone who is trying to rectify their exercise postures and provide a visual keypoint mapping whenever the posture for a particular exercise is bad/wrong.

## Steps to Run


1. **Create a Virtual Environment**: 
    ```
    python -m venv env
    ```

2. **Activate the Virtual Environment**:
   
   - On Windows 
      ```
      env\Scripts\activate
      ```

   - On macOS and Linux
      ```
      source env/bin/activate
      ```

4. **Install Required Packages**: 
    ```
    pip install -r requirements.txt
    ```

5. **Download the YOLOV8 Model**:
    - Download the desired YOLOV8 model and store it under the 'models' folder.
    - You can download ultralytics models using:

      ```
      model = YOLO('yolov8m.pt')
      ```

6. **Run the Flask App**: 
    ```
    flask run
    ```
   
7. **Check the Web Application**:
   
    Once the Flask app is running, open your browser and go to [http://127.0.0.1:5000](http://127.0.0.1:5000) to view the application.

   
    
## Posture Insights Architecture
![image](https://github.com/RohitKrish46/posture-insights-vision/assets/25106707/6b131930-6689-47d5-b977-507813de50d3)

## How it works

- The user initiates the exercise session by accessing the Flask-hosted webpage.
- Subsequently, they select a specific exercise from the available options.
- Upon selecting the exercise, the webcam interface activates, capturing the user's posture in real time.
- Each captured frame undergoes YOLO's pose estimation model analysis, yielding critical information about 17 key joints.
- Based on the exercise type, relevant key points are extracted and employed within heuristic functions to calculate joint angles and motion patterns.
- The heuristic functions then communicate with the Flask server, generating messages if incorrect posture is detected, which are promptly displayed on the Flask UI.


## Playing with YOLOv8’s Pose Estimation Model

I wanted to play with the latest Yolo's pose estimation model for its single-pass architecture eliminates the need for multiple iterations, leading to faster inference speeds. YOLO's ability to detect multiple key points in a single pass aligns well with the complex and dynamic nature of human poses. Additionally, YOLO's deep convolutional neural network architecture has proven effective in handling complex spatial relationships and feature extraction, which are essential for accurate pose estimation.

## Exercise Correction Heuristics 

These are the Exercise for which I have created heuristics for

1. Plank
2. Pushup
3. Bicep Curl

All exercise heuristics revolve around detecting joint angles and joint motion. These angles are derived from the keypoint data obtained through YOLOv8's pose model, while motion details are extracted from the processing of consecutive frames. With this information at hand, we can establish thresholds for both joint angles and joint motion.
