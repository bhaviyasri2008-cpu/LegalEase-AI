import streamlit as st
import google.generativeai as genai

# Gemini API Key - aistudio.google.com la free ah vaangalam
genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="EduGenie", page_icon="📚")
st.title("📚 EduGenie - Your AI Learning Assistant")
st.markdown("Powered by Google Gemini for NASSCOM FSP")

subject = st.selectbox("Subject select pannu", ["General", "Science", "Maths", "Coding", "History", "English"])
level = st.radio("Level", ["School Student", "College Student", "Beginner"])
question = st.text_area("Un kelvi enna? (Ex: Photosynthesis enna?)", height=100)

if st.button("🚀 Explain pannu"):
    if question:
        with st.spinner("Gemini yosikuthu..."):
            prompt = f"""
            You are EduGenie, a friendly tutor for {level}.
            Subject: {subject}
            Question: {question}
            Explain in simple Tamil + English mix (Tanglish), give 1 example, and 2 quiz questions at end.
            """
            response = model.generate_content(prompt)
            st.success("Answer ready!")
            st.write(response.text)
    else:
        st.warning("Kelvi type pannu da!")

st.sidebar.info("Project for SB - Generative AI with Google Cloud Data")