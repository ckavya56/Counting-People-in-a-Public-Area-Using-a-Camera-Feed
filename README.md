# Counting-People-in-a-Public-Area-Using-a-Camera-Feed

This project detects and counts people in a video feed using YOLOv8 and OpenCV.  
It raises an alert when overcrowding is detected for a certain period of time.

## Features
- People detection using YOLOv8
- Crowd counting from video input
- Overcrowding alert system
- Streamlit-based dashboard
- Supports YouTube video links

## Technologies Used
- Python
- YOLOv8
- OpenCV
- Streamlit

## How to Run
1. Install dependencies:
   pip install -r requirements.txt

2. Run the app:
   streamlit run app.py

## Output
- Displays total number of people
- Shows crowd status (Normal / Overcrowded)
- Draws bounding boxes around detected people
