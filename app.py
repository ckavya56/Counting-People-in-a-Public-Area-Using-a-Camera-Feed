# app.py

import cv2
import streamlit as st
from config import MODEL_NAME
from vision.detector import PersonDetector
from vision.tracker import PeopleCounter
from views.dashboard import show_dashboard

st.set_page_config(layout="wide")
st.sidebar.title("Crowd Counting System")

video_file = st.sidebar.file_uploader("Upload a video", type=["mp4", "avi"])

if video_file:
    tfile = open("temp.mp4", "wb")
    tfile.write(video_file.read())

    cap = cv2.VideoCapture("temp.mp4")
    detector = PersonDetector(MODEL_NAME)
    counter = PeopleCounter()

    frame_window = st.image([])

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        detections = detector.detect(frame)
        count = counter.update(detections)

        for x1, y1, x2, y2 in detections:
            cv2.rectangle(frame,
                          (int(x1), int(y1)),
                          (int(x2), int(y2)),
                          (0, 255, 0), 2)

        show_dashboard(count)
        frame_window.image(frame, channels="BGR")

    cap.release()
