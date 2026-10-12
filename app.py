import streamlit as st
from google import genai

# Page Configuration
st.set_page_config(
    page_title="EduGenie",
    page_icon="📚",
    layout="centered"
)

# App Title
st.title("📚 EduGenie - AI Learning Assistant")
st.markdown("Powered by Google Gemini for NASSCOM FSP")

# Sidebar
st.sidebar.title("About EduGenie")
st.sidebar.info(
    "Project for SB - Generative AI with Google Cloud Data"
)

# Get Gemini API Key
try:
    api_key = st.secrets.get("GEMINI_API_KEY", "")
except Exception:
    api_key = ""

# Subject Selection
subject = st.selectbox(
    "📖 Select Subject",
    ["General", "Science", "Maths", "Coding", "History", "English"]
)

# Student Level
level = st.radio(
    "🎓 Student Level",
    ["School Student", "College Student", "Beginner"]
)

# Question Input
question = st.text_area(
    "❓ What is your question?",
    placeholder="Example: What is photosynthesis?",
    height=100
)

# Explain Button
if st.button("🚀 Explain", use_container_width=True):

    if not question.strip():
        st.warning("Please enter your question!")

    elif not api_key:
        st.error(
            "Gemini API Key missing! "
            "Please configure GEMINI_API_KEY in Streamlit Secrets."
        )

    else:
        try:
            with st.spinner("Gemini is thinking..."):

                client = genai.Client(api_key=api_key)

                prompt = f"""
You are EduGenie, a friendly AI tutor.

Student Level: {level}
Subject: {subject}
Student Question: {question}

Instructions:
1. Explain in simple Tamil and English (Tanglish).
2. Give a clear explanation.
3. Provide one easy example.
4. Give two quiz questions at the end.
5. Keep the answer suitable for the student's level.
"""

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

            if response.text:
                st.success("Answer ready! 🎉")
                st.markdown("### 📚 EduGenie Answer")
                st.markdown(response.text)
            else:
                st.warning("No answer received. Please try again.")

        except Exception as e:
            st.error("Something went wrong!")
            st.write("Error details:", str(e))
