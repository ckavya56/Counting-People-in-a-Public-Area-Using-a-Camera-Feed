import cv2
import streamlit as st

from vision.detector import PersonDetector
from vision.tracker import PersonTracker
from vision.counter import PeopleCounter
from database import initialize_database, save_count, get_history

st.set_page_config(page_title="Crowd Counting", layout="wide")
initialize_database()

st.title("Crowd Counting - Video Analytics")
st.sidebar.header("Input")
camera_mode = st.sidebar.checkbox("Use Webcam")



@st.cache_resource
def load_components():
    detector = PersonDetector("yolov8n.pt")
    tracker = PersonTracker()
    counter = PeopleCounter(offset=15)
    return detector, tracker, counter


detector, tracker, counter = load_components()


if camera_mode:
    start = st.button("Start Camera")

    frame_placeholder = st.empty()

    if start:
        cap = cv2.VideoCapture(0)

        while cap.isOpened():

            ret, frame = cap.read()

            if not ret:
                break

            detections = detector.detect(frame)

            people = tracker.update(detections, frame)

            events = counter.update(
                people,
                frame.shape[0]
            )

            for person in people:

                x1, y1, x2, y2 = person["bbox"]
                person_id = person["id"]

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f"ID {person_id}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

            cv2.line(
                frame,
                (0, counter.line_y),
                (frame.shape[1], counter.line_y),
                (255, 0, 0),
                2
            )

            cv2.putText(
                frame,
                f"IN: {counter.total_in}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"OUT: {counter.total_out}",
                (20, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

            inside = counter.total_in - counter.total_out

            cv2.putText(
                frame,
                f"INSIDE: {inside}",
                (20, 110),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 0),
                2
            )

            frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            frame_placeholder.image(
                frame,
                channels="RGB"
            )

            if events:
                save_count(
                    counter.total_in,
                    counter.total_out
                )

        cap.release()

else:
    st.info("Enable 'Use Webcam' from the sidebar.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Entered",
            counter.total_in
        )

    with col2:
        st.metric(
            "Total Exited",
            counter.total_out
        )

    with col3:
        st.metric(
            "Currently Inside",
            counter.total_in - counter.total_out
        )

st.subheader("History")

history = get_history()

if history:
    st.dataframe(
        history,
        column_config={
            "0": "Timestamp",
            "1": "Total In",
            "2": "Total Out",
            "3": "Currently Inside"
        }
    )
else:
    st.info("No history available yet.")