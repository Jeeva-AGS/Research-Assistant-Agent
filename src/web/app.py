import streamlit as st
import sys
import os

# Make src importable
sys.path.append(os.path.abspath(os.path.join(__file__, "../../")))

from agent import run


st.set_page_config(page_title="Research Assistant", layout="wide")

st.title("📚 Personal Research Assistant")

query = st.text_input(
    "Enter your research query",
    placeholder="e.g. Fall detection wearable sensors"
)

if st.button("Research") and query:
    st.subheader("Research Summary")
    status_box = st.empty()
    output_box = st.empty()

    streamed_text = ""
    
    with st.spinner("Working..."):
        for event in run(query):
            if event["type"] == "token":
                status_box.success("Research summary ready")

            if event["type"] == "status":
                status_box.info(event["message"])

            elif event["type"] == "token":
                streamed_text += event["content"]
                output_box.markdown(streamed_text)
