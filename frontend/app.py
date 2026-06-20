import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000/review")

st.set_page_config(page_title="AI Code Review Assistant", layout="wide")
st.title("🧠 AI Code Review Assistant")

st.markdown("Paste your code below and get a review (logic, bugs, optimizations).")

language = st.selectbox("Language", ["python", "javascript", "java", "c++", "other"])

code = st.text_area("Your code", height=300, placeholder="Paste your code here...")

if st.button("Review Code"):
    if not code.strip():
        st.warning("Please paste some code first.")
    else:
        with st.spinner("Reviewing code with LLM..."):
            try:
                payload = {"code": code, "language": language}
                resp = requests.post(BACKEND_URL, json=payload)

                if resp.status_code == 200:
                    data = resp.json()

                    logic = data.get("logic", "").strip()
                    bugs = data.get("bugs", "").strip()
                    optimizations = data.get("optimizations", "").strip()

                    st.subheader("🧩 Logic Explanation")
                    st.write(logic or "_No explanation returned._")

                    st.subheader("🐛 Potential Bugs")
                    st.write(bugs or "_No bugs reported._")

                    st.subheader("⚙️ Suggestions & Optimizations")
                    st.write(optimizations or "_No suggestions provided._")

                else:
                    st.error(f"Backend error: {resp.status_code} - {resp.text}")
            except Exception as e:
                st.error(f"Request failed: {e}")