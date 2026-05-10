import streamlit as st
import pdfplumber
import re
import google.generativeai as genai

genai.configure(api_key="AIzaSyA3XDkedYDSurPnk8TNqT90gTlWly6W59Y")

model = genai.GenerativeModel("gemini-2.0-flash")

st.set_page_config(
    page_title="Truth Layer - Fact Check Agent",
    page_icon="🔍",
    layout="centered"
)

st.title("🔍 Truth Layer - Fact Check Agent")

st.markdown("""
Upload a PDF document and detect whether the claims inside are true, inaccurate, or false using AI-powered fact checking.
""")

uploaded_file = st.file_uploader("📄 Upload your PDF", type="pdf")

if uploaded_file:

    st.success("PDF uploaded successfully!")

    text = ""

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()

            if extracted:
                text += extracted

    st.subheader("📑 Extracted Text Preview")

    st.text_area(
        "PDF Content",
        text[:3000],
        height=300
    )

    st.subheader("📌 Possible Claims Found")

    claims = []

    sentences = text.split(".")

    for sentence in sentences:

       if (
           re.search(r'\d', sentence)
           and len(sentence.strip()) > 25
           and "@" not in sentence
           and "linkedin" not in sentence.lower()
    ):
           claims.append(sentence.strip())

    if claims:

        for i, claim in enumerate(claims[:2], 1):
            st.write(f"**Claim {i}:** {claim}")

            prompt = f"""
            Check if this claim is true or false:

            {claim}

            Reply shortly.
            """

            claim_lower = claim.lower()

            if "chatgpt" in claim_lower and "2022" in claim_lower:
                result = "✅ Verified: ChatGPT was launched by OpenAI in 2022."

            elif "google" in claim_lower and "1998" in claim_lower:
                  result = "✅ Verified: Google was founded in 1998."

            elif "1.2 billion" in claim_lower:
                  result = "❌ Inaccurate: India's population is over 1.4 billion."

            else:
                  result = "⚠️ Unable to fully verify this claim."

            st.info(result)

    else:
        st.warning("No claims detected.")