import streamlit as st
from google import genai
import fitz  # PyMuPDF
from docx import Document
import io

# --- 1. UI SETUP ---
st.set_page_config(page_title="Physics Board Bot 2026", page_icon="🍎")
st.title("🍎 Physics Board Exam Expert")
st.markdown("---")

# --- 2. SIDEBAR FOR API KEY ---
with st.sidebar:
    st.header("Settings")
    user_api_key = st.text_input("Gemini API Key daalein:", type="password")
    st.info("Aapki key surakshit hai.")

# --- 3. MAIN LOGIC ---
uploaded_file = st.file_uploader("Chapter PDF Upload Karein", type="pdf")

if uploaded_file and user_api_key:
    # PDF se text nikalna
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    full_text = ""
    for page in doc:
        full_text += page.get_text()

    st.success(f"PDF Uploaded! Total Pages: {len(doc)}")

    if st.button("Deep Notes & Question Bank Taiyaar Karein"):
        try:
            # Gemini Client Setup
            client = genai.Client(api_key=user_api_key)
            
            # Master Prompt - Focus on Depth & 2026 Pattern
            master_prompt = f"""
            You are a Senior Physics Board Examiner. Create "Deep Text-Only Notes" for the provided text.
            
            STRICT RULES:
            - NO IMAGES & NO LaTeX: Write equations simply (e.g., V = I x R, H = I squared R t).
            - NO STARS: Use '-' for bullets. Do NOT use '*'.
            - 2026 PATTERN: After each topic, add 1 Case-Based Question, 2 Assertion-Reason Questions, and 3 Competency Questions.
            - SYLLABUS: Cover Electricity topics like Ohm's Law, Resistance, Heating Effect, and Power in detail.
            - DEPTH: Explain the 'Why' for every concept. Iterate topic-by-topic and do NOT move to the next topic until depth is met.

            Text to process:
            {full_text[:15000]} 
            """
            
            # API Call - Keyword arguments are safe for Python
            response = client.models.generate_content(
                model="gemini-1.5-flash", 
                contents=master_prompt
            )
            
            # Result dikhana
            st.markdown("### 📝 Generated Deep Notes")
            st.write(response.text)

            # --- 4. EXPORT TO WORD ---
            word_doc = Document()
            word_doc.add_heading('Class 10 Physics: Deep Exam Notes & 2026 Question Bank', 0)
            word_doc.add_paragraph(response.text)
            
            # Save to memory buffer
            bio = io.BytesIO()
            word_doc.save(bio)
            
            st.download_button(
                label="📥 Final Word File Download Karein",
                data=bio.getvalue(),
                file_name="Physics_Board_Expert_Notes.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

        except Exception as e:
            st.error(f"Error: {e}")
else:
    st.info("Aage badhne ke liye apni API Key daalein aur PDF upload karein.")
