import streamlit as st
import cv2
import numpy as np
from PIL import Image

from image_processing import (
    convert_to_grayscale,
    detect_edges,
    apply_threshold
)

from object_detection import ObjectDetector

from image_analysis import (
    get_image_information,
    summarize_detections
)


# -----------------------------
# PAGE CONFIGURATION
# -----------------------------

st.set_page_config(
    page_title="Smart CV Analyzer",
    page_icon="👁️",
    layout="wide"
)


# -----------------------------
# CUSTOM CSS
# -----------------------------

st.markdown("""
<style>

.main-title {
    font-size: 38px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 17px;
    color: #666;
    margin-bottom: 25px;
}

.section-title {
    font-size: 24px;
    font-weight: 650;
    margin-top: 10px;
}

.result-card {
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #ddd;
    background-color: #fafafa;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# HEADER
# -----------------------------

st.markdown(
    '<div class="main-title">👁️ Smart Computer Vision Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Analyze images using classical Computer Vision and YOLO-based object detection.'
    '</div>',
    unsafe_allow_html=True
)


# -----------------------------
# SIDEBAR
# -----------------------------

with st.sidebar:

    st.header("⚙️ Controls")

    uploaded_file = st.file_uploader(
        "Upload an image",
        type=["jpg", "jpeg", "png"]
    )

    st.divider()

    st.write("### Supported Operations")

    st.write("✓ Grayscale")
    st.write("✓ Edge Detection")
    st.write("✓ Thresholding")
    st.write("✓ Object Detection")
    st.write("✓ Image Analysis")


# -----------------------------
# MAIN APPLICATION
# -----------------------------

if uploaded_file is None:

    st.info(
        "👈 Upload a JPG, JPEG, or PNG image from the sidebar to begin."
    )

    st.markdown("### How it works")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 01")
        st.write("Upload an image")

    with col2:
        st.markdown("### 02")
        st.write("Apply Computer Vision")

    with col3:
        st.markdown("### 03")
        st.write("Analyze the results")

else:

    # -----------------------------
    # LOAD IMAGE
    # -----------------------------

    image = Image.open(uploaded_file).convert("RGB")

    image_np = np.array(image)

    image_cv = cv2.cvtColor(
        image_np,
        cv2.COLOR_RGB2BGR
    )


    # -----------------------------
    # ORIGINAL IMAGE
    # -----------------------------

    st.markdown(
        '<div class="section-title">Original Image</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.image(
            image,
            caption="Uploaded Image",
            width=500
        )


    st.divider()


    # -----------------------------
    # TABS
    # -----------------------------

    tab1, tab2, tab3 = st.tabs([
        "🖼️ Image Processing",
        "🎯 Object Detection",
        "📊 Image Analysis"
    ])


    # ==========================================================
    # MODULE 1
    # ==========================================================

    with tab1:

        st.subheader("Image Processing")

        st.write(
            "Apply classical Computer Vision techniques to understand "
            "different representations of the image."
        )

        gray = convert_to_grayscale(image_cv)

        edges = detect_edges(image_cv)

        threshold = apply_threshold(image_cv)


        col1, col2, col3 = st.columns(3)


        with col1:

            st.markdown("**Grayscale**")

            st.image(
                gray,
                width=280
            )


        with col2:

            st.markdown("**Canny Edge Detection**")

            st.image(
                edges,
                width=280
            )


        with col3:

            st.markdown("**Thresholding**")

            st.image(
                threshold,
                width=280
            )


    # ==========================================================
    # MODULE 2
    # ==========================================================

    with tab2:

        st.subheader("Object Detection")

        st.write(
            "YOLO identifies objects in the uploaded image and "
            "provides bounding boxes with confidence scores."
        )


        with st.spinner("Detecting objects..."):

            detector = ObjectDetector()

            results, detections = detector.detect(image_np)


        annotated_image = results[0].plot()


        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:

            st.image(
                annotated_image,
                caption="Detected Objects",
                width=550
            )


        st.divider()


        if detections:

            st.subheader("Detected Objects")


            for detection in detections:

                label = detection["label"]

                confidence = detection["confidence"]


                st.write(
                    f"**{label.title()}** — "
                    f"{confidence:.1%} confidence"
                )

        else:

            st.warning("No objects detected.")


    # ==========================================================
    # MODULE 3
    # ==========================================================

    with tab3:

        st.subheader("Image Analysis")

        info = get_image_information(image_cv)

        summary = summarize_detections(detections)


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Width",
                f"{info['width']} px"
            )


        with col2:

            st.metric(
                "Height",
                f"{info['height']} px"
            )


        with col3:

            st.metric(
                "Objects",
                len(detections)
            )


        st.divider()


        if summary:

            st.subheader("Detection Summary")


            for label, count in summary.items():

                st.write(
                    f"**{label.title()}**: {count}"
                )