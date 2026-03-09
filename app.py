import streamlit as st
import pandas as pd
import numpy as np
import cv2
from PIL import Image
import pickle
import tensorflow as tf

# --- PAGE CONFIG ---
st.set_page_config(page_title="OncoSight: pCR Predictor", layout="wide")
st.title("OncoSight: Multimodal pCR Triage Dashboard")
st.markdown("Upload a patient's histology patch and input clinical data to predict Neoadjuvant Chemotherapy response.")

# --- LOAD MODELS ---
@st.cache_resource
def load_pipeline():
    # Replace these with your actual saved file paths
    preprocessor = pickle.load(open('preprocessor.pkl', 'rb'))
    model = tf.keras.models.load_model('keras_pcr_model.h5')
    return None, None 

preprocessor, model = load_pipeline()

def process_uploaded_image(uploaded_file):
    # Convert Streamlit upload to OpenCV image
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 1. Feature Extraction (Your Logic)
    # We subtract Red from Blue to highlight Hematoxylin (nuclei)
    n_data = cv2.subtract(img[:,:,2], img[:,:,0]) 
    e_data = cv2.Canny(img, 100, 200)
    
    # 2. Metrics Calculation
    _, binary_n = cv2.threshold(n_data, 30, 255, cv2.THRESH_BINARY)
    density = np.mean(binary_n > 0)
    complexity = np.mean(e_data > 0)
    contours, _ = cv2.findContours(binary_n, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    clump_count = len(contours)

    # 3. Draw Bounding Boxes on the image for the UI
    annotated_img = img_rgb.copy()
    for cnt in contours:
        if cv2.contourArea(cnt) > 10: 
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(annotated_img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    return annotated_img, density, complexity, clump_count

# --- DASHBOARD LAYOUT ---
col1, col2, col3 = st.columns([1, 1.5, 1])

# COLUMN 1: Clinical Tabular Inputs
with col1:
    st.header("Clinical Data")
    age = st.slider("Age", 20, 90, 50)
    tumor_size = st.number_input("cT (Size, mm)", value=25.0)
    er_pct = st.slider("ER (%)", 0, 100, 80)
    pr_pct = st.slider("PR (%)", 0, 100, 60)
    
    her2 = st.selectbox("HER2 Status", options=[0, 1], format_func=lambda x: "Positive (1)" if x==1 else "Negative (0)")
    cn = st.selectbox("cN (Node Status)", options=[0, 1], format_func=lambda x: "Positive (1)" if x==1 else "Negative (0)")
    
    grade = st.selectbox("Grade Nottingham", options=[1, 2, 3])
    histology = st.selectbox("Histology", options=[0, 1, 2], format_func=lambda x: {0:"IDC", 1:"ILC", 2:"IMC"}[x])

# COLUMN 2: The Pathology Viewer
with col2:
    st.header("Histology Biopsy Patch")
    uploaded_file = st.file_uploader("Upload an image patch (.png, .jpg)", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        # Run the processing bridge
        annotated_img, n_dens, e_comp, c_count = process_uploaded_image(uploaded_file)
        
        # Display the image with bounding boxes
        st.image(annotated_img, caption="Automated Computer Vision Detection", use_container_width=True)
        
        # Display extracted metrics
        st.info(f"**Extracted Biomarkers:** \n\n Nuclear Density: {n_dens:.4f} | Edge Complexity: {e_comp:.4f} | Clumps per Patch: {c_count}")

# COLUMN 3: AI Prediction
with col3:
    st.header("AI Prognosis")
    
    if uploaded_file is not None:
        if st.button("Generate pCR Prediction", type="primary", use_container_width=True):
            # Gather all 11 inputs
            input_data = pd.DataFrame({
                'Age': [age],
                'cT (Size, mm)': [tumor_size],
                'ER (%)': [er_pct],
                'PR (%)': [pr_pct],
                'Img_Nuclear_Density': [n_dens],
                'Img_Edge_Complexity': [e_comp],
                'Img_Clump_Count_Per_Patch': [c_count],
                'HER2 (0=neg; 1=pos)': [her2],
                'cN (0=neg; 1=pos)': [cn],
                'Grade Nottingham': [grade],
                'Histology (0=IDC; 1=ILC; 2=IMC)': [histology]
            })
            
            # Predict (replace mock with actual when ready)
            # processed_data = preprocessor.transform(input_data)
            # prediction_prob = model.predict(processed_data)[0][0]
            prediction_prob = 0.8549 
            
            st.metric(label="pCR Probability", value=f"{prediction_prob * 100:.1f}%")
            
            if prediction_prob >= 0.5:
                st.success("High likelihood of Pathologic Complete Response.")
            else:
                st.error("Low likelihood of Complete Response.")
    else:
        st.warning("Please upload a biopsy image.")