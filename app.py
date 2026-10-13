import streamlit as st
from google import genai
from datetime import date

# Page Configuration
st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="centered"
)

# App Title
st.title("⚖️ LegalEase - AI Legal Document Generator")

st.caption(
    "Disclaimer: AI-generated draft only. "
    "Review by a qualified lawyer is recommended."
)

# Gemini API Configuration
api_key = st.secrets.get("GEMINI_API_KEY", "")

if not api_key:
    st.warning(
        "Gemini API key is missing. "
        "Please configure GEMINI_API_KEY in Streamlit secrets."
    )
    st.stop()

client = genai.Client(api_key=api_key)

# Document Details
col1, col2 = st.columns(2)

with col1:
    doc_type = st.selectbox(
        "Document Type",
        [
            "Rental Agreement",
            "NDA - Non-Disclosure Agreement",
            "Employment Offer Letter",
            "Affidavit",
            "Service Agreement"
        ]
    )

with col2:
    doc_date = st.date_input("Date", date.today())

st.divider()

# Party Details
st.subheader("Party Details")

p1_name = st.text_input("Party 1 / Owner / Company Name")
p1_address = st.text_input("Party 1 Address")

p2_name = st.text_input("Party 2 / Tenant / Employee Name")
p2_address = st.text_input("Party 2 Address")

extra = st.text_area(
    "Important Clauses / Salary / Rent Amount / Duration",
    placeholder="Enter details in Tamil or English...",
    height=120
)

# Generate Document
if st.button("📄 Generate Legal Document"):

    if not p1_name.strip() or not p2_name.strip() or not extra.strip():
        st.warning(
            "Please enter both party names and the important details."
        )

    else:
        prompt = f"""
You are LegalEase, an AI assistant that drafts legal documents.

Draft a preliminary {doc_type} dated {doc_date}.

Party 1:
Name: {p1_name}
Address: {p1_address}

Party 2:
Name: {p2_name}
Address: {p2_address}

Additional details:
{extra}

Instructions:
1. Use clear, professional English.
2. Organize the document with suitable headings.
3. Include the parties' details and relevant terms and conditions.
4. Include termination clauses where appropriate.
5. Include signature sections for the parties.
6. Do not invent missing facts, laws, or legal requirements.
7. Identify details that need verification by a lawyer.
8. State that the document is an AI-generated draft and requires
   review by a qualified Indian lawyer.
9. Do not claim that the draft is legally compliant or enforceable
   without verification.

Generate the preliminary document.
"""

        try:
            with st.spinner("Drafting your document..."):

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                if response.text:
                    document = response.text

                    st.success("Document Generated Successfully!")

                    st.subheader("📄 Generated Legal Document")

                    st.text_area(
                        "Your Document",
                        value=document,
                        height=400
                    )

                    st.download_button(
                        label="⬇️ Download as TXT",
                        data=document,
                        file_name="LegalEase_Document.txt",
                        mime="text/plain"
                    )

                else:
                    st.error(
                        "The AI returned an empty response. Please try again."
                    )

        except Exception as e:
            st.error(
                "Unable to generate the document. "
                "Please check your API key, internet connection, "
                "and Gemini API access."
            )
            st.code(str(e))

# Sidebar
st.sidebar.title("About LegalEase")

st.sidebar.info(
    "AI-powered preliminary legal document drafting."
)

st.sidebar.markdown(
    "**For:** NASSCOM FSP - Generative AI with Google Cloud Data"
)
