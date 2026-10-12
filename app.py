import streamlit as st
from google import genai
st.set_page_config(
    page_title="EduGenie",
    page_icon="📚",
    layout="centered",
)
def get_gemini_api_key() -> str:
    # Replit Secrets/environment variable first
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if api_key:
        return api_key
    # Also supports Streamlit Secrets
    try:
        return str(st.secrets.get("GEMINI_API_KEY", "")).strip()
    except Exception:
        return ""
st.title("📚 EduGenie - AI Learning Assistant")
st.markdown("Powered by Google Gemini for NASSCOM FSP")
with st.sidebar:
    st.title("About EduGenie")
    st.info("Project for SB - GenAI with Google Cloud Data")
subject = st.selectbox(
    "📖 Select Subject",
    ["General", "Science", "Maths", "Coding", "History", "English"],
)
level = st.radio(
    "🎓 Student Level",
    ["School Student", "College Student", "Beginner"],
)
question = st.text_area(
    "❓ What is your question?",
    placeholder="Example: What is photosynthesis?",
    height=100,
)
if st.button("🚀 Explain", use_container_width=True):
    if not question.strip():
        st.warning("Please enter your question.")
    else:
        api_key = get_gemini_api_key()
        if not api_key:
            st.error(
                "Gemini API key missing. Add GEMINI_API_KEY in Replit Secrets "
                "or Streamlit Secrets."
            )
        else:
            prompt = f"""
You are EduGenie, a friendly AI tutor.
Student Level: {level}
Subject: {subject}
Student Question: {question.strip()}
Instructions:
1. Explain in simple Tamil and English (Tanglish).
2. Give a clear, student-level explanation.
3. Provide one easy example.
4. Give exactly two quiz questions at the end.
5. Keep the answer suitable for the student's level.
"""
            try:
                with st.spinner("Gemini is thinking..."):
                    client = genai.Client(api_key=api_key)
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt,
                    )
                answer = response.text
                if answer and answer.strip():
                    st.success("Answer ready! 🎉")
                    st.markdown("### 📚 EduGenie Answer")
                    st.markdown(answer)
                else:
                    st.warning("Gemini returned an empty answer. Please try again.")
            except Exception as error:
                st.error("Gemini couldn't generate an answer. Check the API key and try again.")
                with st.expander("Technical error details"):
                    st.code(str(error))
