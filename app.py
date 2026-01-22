import streamlit as st
import cv2
import time
import os
import numpy as np
from ultralytics import YOLO
import yt_dlp

# -----------------------------------
# CONFIGURATION
# -----------------------------------
VIDEO_FILE = "crowd_video.mp4"
CONFIDENCE = 0.4
SKIP_FRAMES = 3  # Skip frames for better performance

# -----------------------------------
# STREAMLIT PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="Crowd Alert System",
    layout="wide"
)

st.title("🚨 Overcrowding Detection System")
st.caption("YOLOv8 + OpenCV + Streamlit")

# -----------------------------------
# SIDEBAR SETTINGS
# -----------------------------------
st.sidebar.header("⚙️ Settings")

threshold = st.sidebar.slider(
    "Max Allowed People",
    min_value=1,
    max_value=100,
    value=20
)

alert_duration = st.sidebar.slider(
    "Alert if overcrowded for (seconds)",
    min_value=1,
    max_value=10,
    value=3
)

yt_url = st.text_input("📺 Paste YouTube Video URL")

# -----------------------------------
# YOUTUBE VIDEO DOWNLOAD FUNCTION
# -----------------------------------
def download_youtube_video(url):
    if os.path.exists(VIDEO_FILE):
        os.remove(VIDEO_FILE)

    ydl_opts = {
        "format": "mp4",
        "outtmpl": VIDEO_FILE,
        "quiet": True,
        "noplaylist": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# -----------------------------------
# LOAD YOLO MODEL (CACHED)
# -----------------------------------
@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")

model = load_model()

# -----------------------------------
# PEOPLE COUNTING FUNCTION
# -----------------------------------
def count_people(frame):
    results = model(frame, conf=CONFIDENCE, verbose=False)
    count = 0

    for r in results:
        for box in r.boxes:
            # Class 0 corresponds to 'person'
            if int(box.cls[0]) == 0:
                count += 1
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

    return count, frame

# -----------------------------------
# START VIDEO ANALYSIS
# -----------------------------------
if st.button("▶ Start Analysis") and yt_url:

    with st.spinner("Downloading YouTube video..."):
        download_youtube_video(yt_url)

    cap = cv2.VideoCapture(VIDEO_FILE)

    # Dashboard metrics
    col1, col2, col3 = st.columns(3)
    people_metric = col1.empty()
    status_metric = col2.empty()
    timer_metric = col3.empty()

    frame_placeholder = st.empty()

    overcrowd_start = None
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % SKIP_FRAMES != 0:
            continue

        frame = cv2.resize(frame, (960, 540))

        count, annotated_frame = count_people(frame)

        # -----------------------------------
        # ALERT LOGIC
        # -----------------------------------
        if count > threshold:
            if overcrowd_start is None:
                overcrowd_start = time.time()
            elapsed = int(time.time() - overcrowd_start)
        else:
            overcrowd_start = None
            elapsed = 0

        # -----------------------------------
        # UPDATE UI
        # -----------------------------------
        people_metric.metric("👥 People Count", count)

        if elapsed >= alert_duration:
            status_metric.error("🚨 OVERCROWDING ALERT")
        else:
            status_metric.success("✅ Normal Crowd")

        timer_metric.metric("⏱ Overcrowded (sec)", elapsed)

        frame_placeholder.image(
            annotated_frame,
            channels="BGR",
            use_container_width=True
        )

    cap.release()
    st.success("✅ Video Analysis Completed")

# -----------------------------------
# FOOTER
# -----------------------------------
st.markdown("---")
st.markdown("Built with Streamlit, YOLOv8, and OpenCV")
