import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import streamlit as st
import time
import pdfkit
from datetime import datetime

# ✅ Load Data
df_project = pd.read_csv(r"C:\Users\santh\OneDrive\Desktop\finale\Project.csv")
df_dev = pd.read_csv(r"C:\Users\santh\OneDrive\Desktop\finale\developers.csv")
df_lead = pd.read_csv(r"C:\Users\santh\OneDrive\Desktop\finale\Lead.csv")
df_scrum = pd.read_csv(r"C:\Users\santh\OneDrive\Desktop\finale\Scrummaster.csv")

# ✅ Download NLTK Resources
nltk.download("punkt")
nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

# ✅ Preprocess Text
def preprocess_text(text):
    words = word_tokenize(text.lower())
    return [word for word in words if word.isalnum() and word not in stop_words]

# ✅ Keywords
keywords = {
    "Lead": ["lead", "team lead", "head"],
    "Scrum Master": ["scrum", "agile"],
    "Developer": ["developer", "engineer"],
    "Project": ["project", "timeline"]
}

# ✅ Detect Category
def detect_category(query):
    query_tokens = preprocess_text(query)
    for category, words in keywords.items():
        if any(word in query_tokens for word in words):
            return category
    return None

# ✅ Search Data
def search_info(query, category):
    datasets = {
        "Lead": df_lead,
        "Scrum Master": df_scrum,
        "Developer": df_dev,
        "Project": df_project
    }
    
    df = datasets.get(category)
    if df is None:
        return "❌ No relevant information found."

    for _, row in df.iterrows():
        row_text = " ".join(str(value) for value in row)
        row_tokens = preprocess_text(row_text)
        if any(token in row_tokens for token in preprocess_text(query)):
            return row.to_dict()
    return f"❌ No matching {category} data found."

# ✅ Generate PDF

def generate_pdf():
    html_content = "<h2>Chat History</h2>"
    for message in st.session_state.history:
        if message.startswith("User:"):
            html_content += f"<p><b>User:</b> {message[6:]}</p>"
        elif message.startswith("AI:"):
            html_content += f"<p><b>AI:</b> {message[4:]}</p>"

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    pdf_path = f"chat_history_{timestamp}.pdf"

    config = pdfkit.configuration(wkhtmltopdf=r"C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
    pdfkit.from_string(html_content, pdf_path, configuration=config)
    return pdf_path

# ✅ Streamlit Page
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
    }
    .chat-container {
        background-color: #f4f4f4;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 5px 5px 20px rgba(0,0,0,0.1);
    }
    .user-bubble {
        background-color: #007bff;
        color: white;
        border-radius: 20px;
        padding: 10px;
        text-align: right;
        margin-bottom: 10px;
    }
    .bot-bubble {
        background-color: #e0e0e0;
        border-radius: 20px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .input-box {
        border: 1px solid #007bff;
        border-radius: 20px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ✅ Chat Section
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
if 'history' not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("Ask me about projects, developers, etc.", key="user_query")

if st.button("Search 💬"):
    if user_input.strip():
        st.session_state.history.append(f"User: {user_input}")
        category = detect_category(user_input)
        if category:
            result = search_info(user_input, category)
            if isinstance(result, dict):
                ai_response = f"✅ {category} Data Found:<br>"
                for key, value in result.items():
                    ai_response += f"<b>{key}:</b> {value}<br>"
            else:
                ai_response = result
        else:
            ai_response = "❌ Category not recognized."
        st.session_state.history.append(f"AI: {ai_response}")

# ✅ Show Chat History
for message in st.session_state.history:
    if message.startswith("User:"):
        st.markdown(f"<div class='user-bubble'>{message[6:]}</div>", unsafe_allow_html=True)
    elif message.startswith("AI:"):
        st.markdown(f"<div class='bot-bubble'>{message[4:]}</div>", unsafe_allow_html=True)

# ✅ Download Chat History
if st.button("📥 Download Chat History"):
    pdf_file = generate_pdf()
    with open(pdf_file, "rb") as f:
        st.download_button("Download PDF", f, file_name=pdf_file)