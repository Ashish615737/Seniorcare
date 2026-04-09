import streamlit as st
import cv2
import numpy as np
import torch
import tensorflow as tf
from PIL import Image
import tempfile

# Custom CSS styling
st.markdown("""
    <style>
        /* Main container styling */
        .main {
            background-color: #f5f7f9;
            padding: 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }

        /* Header styling */
        .title-container {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        .main-title {
            color: white;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        .sub-title {
            color: #e0e0e0;
            font-size: 1.5rem;
            font-weight: 500;
        }

        /* Section styling */
        .section-container {
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            margin-bottom: 2rem;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }

        .section-title {
            color: #1e3c72;
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 1rem;
            border-bottom: 2px solid #1e3c72;
            padding-bottom: 0.5rem;
        }

        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 5px;
            font-weight: 500;
            transition: all 0.3s ease;
            width: 200px;
            margin: 0.5rem;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        /* File uploader styling */
        .uploadedFile {
            border: 2px dashed #1e3c72;
            border-radius: 5px;
            padding: 1rem;
            text-align: center;
            margin-bottom: 1rem;
        }

        /* Video container styling */
        .video-container {
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin: 1rem 0;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }

        /* Status message styling */
        .status-message {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
            border-left: 4px solid #1e3c72;
        }

        /* Button container */
        .button-container {
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin: 1rem 0;
        }

        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        /* Responsive design */
        @media screen and (max-width: 768px) {
            .main-title {
                font-size: 2rem;
            }
            .sub-title {
                font-size: 1.25rem;
            }
            .section-container {
                padding: 1rem;
            }
        }
    </style>
""", unsafe_allow_html=True)

# Set page config


# Initialize session state
if 'model' not in st.session_state:
    st.session_state.model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

if 'model1' not in st.session_state:
    st.session_state.model1 = tf.keras.models.load_model("PhysioNet.h5")

if 'webcam_active' not in st.session_state:
    st.session_state.webcam_active = False

# Define exercise labels
labels = ['Butterfly', 'Calf raises', 'goddess', 'Hand raises', 'Knee pushups',
          'Lowerback strecth', 'Shoulder press', 'shoulder stretch', 'situps',
          'tree', 'wallChair', 'Warmup']


def process_frame(frame, flip=False):
    if flip:
        frame = cv2.flip(frame, 1)

    image = cv2.resize(frame, (224, 224))
    results = np.argmax(st.session_state.model1.predict(np.array([image])))
    detections = st.session_state.model(frame)
    person_detections = detections.pred[0][detections.pred[0][:, 5] == 0]

    for det in person_detections:
        x1, y1, x2, y2, conf, _ = det.tolist()
        label = f'Score: {conf:.2f} - Exercise: {labels[results]}'
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.putText(frame, label, (0, 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 2)

    return frame


# Custom title container
st.markdown("""
    <div class="title-container">
        <div class="main-title">KALASALINGAM ACADEMY OF RESEARCH AND EDUCATION</div>
        <div class="sub-title">Exercise Detection System</div>
    </div>
""", unsafe_allow_html=True)

# Upload Video Section
st.markdown('<div class="section-container">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Upload Video</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose a video file", type=['mp4', 'avi'], key="video_uploader")
video_placeholder = st.empty()

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    cap = cv2.VideoCapture(tfile.name)

    if st.button("Process Video", key="process_video"):
        st.markdown('<div class="video-container">', unsafe_allow_html=True)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            processed_frame = process_frame(frame, flip=False)
            processed_frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            video_placeholder.image(processed_frame_rgb)
        cap.release()
        st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Webcam Section
st.markdown('<div class="section-container">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Webcam Feed</div>', unsafe_allow_html=True)

webcam_placeholder = st.empty()

# Centered buttons
st.markdown('<div class="button-container">', unsafe_allow_html=True)
start_button = st.button("Start Webcam", key="start_webcam")
stop_button = st.button("Stop Webcam", key="stop_webcam")
st.markdown('</div>', unsafe_allow_html=True)

if start_button:
    st.session_state.webcam_active = True
if stop_button:
    st.session_state.webcam_active = False

if st.session_state.webcam_active:
    st.markdown('<div class="video-container">', unsafe_allow_html=True)
    cap = cv2.VideoCapture(0)

    while st.session_state.webcam_active:
        ret, frame = cap.read()
        if not ret:
            st.markdown('<div class="status-message">Failed to access webcam</div>',
                        unsafe_allow_html=True)
            st.session_state.webcam_active = False
            break

        processed_frame = process_frame(frame, flip=True)
        processed_frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
        webcam_placeholder.image(processed_frame_rgb)

    cap.release()
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style="text-align: center; margin-top: 2rem; padding: 1rem; background: #f8f9fa; border-radius: 8px;">
        <p style="color: #666; font-size: 0.9rem;">© 2024 Kalasalingam Academy of Research and Education</p>
    </div>
""", unsafe_allow_html=True)