import pandas as pd
import streamlit as st

from src.serving.model import BertPredictor

def init_state():
    if 'history' not in st.session_state:
        st.session_state['history'] = []

@st.cache_resource()
def get_model() -> BertPredictor:
    return BertPredictor.from_model_registry()

predictor = get_model()

def prediction():
    st.subheader("Fake news prediction")
    input_sent = st.text_area("Type an English news here", value="This is example input", height=150)
    if st.button("Run Inference"):
        pred = predictor.predict([input_sent])
        st.session_state['history'].append({'Input': input_sent, 'Prediction': pred})
        st.write("**Prediction:**", pred[0])
        st.write("**Prediction History**")
        for item in reversed(st.session_state['history']):
            st.text(f"Input: {item['Input']}\nPrediction: {item['Prediction'][0]}\n")

def batch_pred():
    st.subheader("Batch Prediction from CSV")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    if uploaded_file:
        dataframe = pd.read_csv(uploaded_file)
        st.markdown("#### Input dataframe")
        st.dataframe(dataframe)

        dataframe_with_pred = predictor.run_inference_on_dataframe(dataframe)
        st.markdown("#### Result dataframe")
        st.dataframe(dataframe_with_pred)

def main():
    st.title("BERT Model Prediction Service")
    init_state()
    prediction()

if __name__ == "__main__":
    main()
