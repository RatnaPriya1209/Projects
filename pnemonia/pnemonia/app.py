import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

st.title("Pneumonia Detector")
st.write("PROJECT ON PNEUMONIA DETECTION")

uploaded_image = st.file_uploader("Choose a chest X-ray image", type=["png", "jpg", "jpeg"])

@st.cache_data() #temporary memory 
def get_model():
    return tf.keras.models.load_model('pneumonia_model.h5')

model = get_model()
IMG_SIZE = 64
class_name = ['Normal', 'Pneumonia']

def predict(img):
    img = img.resize((IMG_SIZE, IMG_SIZE))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array)[0][0]
    label = class_name[1] if prediction > 0.5 else class_name[0]
    confidence = prediction if prediction > 0.5 else 1 - prediction
    return f"{label} ({confidence*100:.2f}% Confidence)"

if uploaded_image is not None:
    image = Image.open(uploaded_image).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)
    output = predict(image)
    st.write(output)
#st,markdown(f"prediction:{label}")
#st.markdown(f"confidence:{confidence:.2f}")