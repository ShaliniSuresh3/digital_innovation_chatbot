import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import streamlit as st
import time
import pdfkit
from datetime import datetime

# Set Page Configuration
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")

# Load Data
df_project = pd.read_csv(r"C:\Users\santh\OneDrive\Desktop\finale\Project.csv")
df_dev = pd.read_csv(r"C:\Users\santh\OneDrive\Desktop\finale\developers.csv")
df_lead = pd.read_csv(r"C:\Users\santh\OneDrive\Desktop\finale\Lead.csv")
df_scrum = pd.read_csv(r"C:\Users\santh\OneDrive\Desktop\finale\Scrummaster.csv")

# Download NLTK Resources
nltk.download("punkt")
nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

# Preprocess Text
def preprocess_text(text):
    words = word_tokenize(text.lower())
    return [word for word in words if word.isalnum() and word not in stop_words]

# Define Keywords
keywords = {
    "Lead": ["lead", "leader", "team lead", "head", "management"],
    "Scrum Master": ["scrum", "scrum master", "agile", "sprint"],
    "Developer": ["developer", "engineer", "programmer", "coder"],
    "Project": ["project", "timeline", "budget", "progress", "metrics"]
}

# Function to Detect Category
def detect_category(query):
    query_tokens = preprocess_text(query)
    for category, words in keywords.items():
        if any(word in query_tokens for word in words):
            return category
    return None

# Function to Search Relevant Data
def search_info(query, category):
    dataset_mapping = {
        "Lead": df_lead,
        "Scrum Master": df_scrum,
        "Developer": df_dev,
        "Project": df_project
    }
    df = dataset_mapping.get(category)
    if df is None:
        return "❌ No relevant information found."

    query_tokens = preprocess_text(query)
    for _, row in df.iterrows():
        row_text = " ".join(str(value) for value in row)
        row_tokens = preprocess_text(row_text)
        if any(token in row_tokens for token in query_tokens):
            return row.to_dict()
    return f"❌ No matching {category} data found."

#  Function to Generate PDF
def generate_pdf():
    html_content = "<h2>Chat History</h2>"
    for message in st.session_state.history:
        if message.startswith("User:"):
            html_content += f"<p><b>User:</b> {message[6:]}</p>"
        elif message.startswith("AI:"):
            html_content += f"<p><b>AI:</b> {message[4:]}</p>"

    #  Generate PDF Path
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    pdf_path = f"chat_history_{timestamp}.pdf"

    #  PDF Configuration
    config = pdfkit.configuration(wkhtmltopdf=r"C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
    pdfkit.from_string(html_content, pdf_path, configuration=config)
    return pdf_path

#  Streamlit Sidebar (Chatbot Info)

st.sidebar.title("🤖 Chatbot Info")
st.sidebar.write("""
This AI chatbot provides **answers** based on:
- **Leads**
- **Scrum Masters**
- **Developers**
- **Project Metrics**

✅ It can generate PDF chat history on demand.
""")

#  Custom CSS (UI Design)
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://source.unsplash.com/1600x900/?technology,abstract");
        background-size: cover;
    }
    .chat-container {
        width: 60%;
        margin: auto;
        background: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 5px 5px 20px rgba(0,0,0,0.2);
    }
    .chat-bubble {
        background: #0078ff;
        color: white;
        padding: 10px;
        border-radius: 15px;
        max-width: 80%;
        margin-bottom: 10px;
    }
    .user-bubble {
        background: #e6e6e6;
        color: black;
        padding: 10px;
        border-radius: 15px;
        max-width: 80%;
        text-align: right;
        margin-left: auto;
    }
    </style>
""", unsafe_allow_html=True)

#  Initialize Chat History
if 'history' not in st.session_state:
    st.session_state.history = []

if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

# Chat UI
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center;'>🤖 AI Chatbot</h2>", unsafe_allow_html=True)

#  User Input
user_input = st.text_input("🔍 Ask me about projects, developers, or teams...", value=st.session_state.user_input, key="user_query")

#  Search Button
if st.button("Search 💬"):
    if user_input.strip():
        # ✅ Add user input to history
        st.session_state.history.append(f"User: {user_input}")

        # ✅ Typing Animation
        typing_placeholder = st.empty()
        typing_placeholder.markdown("<div class='chat-bubble'>AI is typing...</div>", unsafe_allow_html=True)
        time.sleep(1.5)
        typing_placeholder.empty()

        # ✅ Detect Category
        category = detect_category(user_input)
        if category:
            result = search_info(user_input, category)
            if isinstance(result, dict):
                ai_response = f"✅ {category} Data Found:<br>"
                for key, value in result.items():
                    ai_response += f"<strong>{key}:</strong> {value}<br>"
            else:
                ai_response = result
        else:
            ai_response = "❌ Sorry, I couldn't determine the category."

        # ✅ Add AI Response to History
        st.session_state.history.append(f"AI: {ai_response}")

#  Display Chat History
for message in st.session_state.history:
    if message.startswith("User:"):
        st.markdown(f"<div class='user-bubble'>{message[6:]}</div>", unsafe_allow_html=True)
    elif message.startswith("AI:"):
        st.markdown(f"<div class='chat-bubble'>{message[4:]}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

#  Download Chat History
if st.button("📥 Download Chat History as PDF"):
    pdf_file = generate_pdf()
    with open(pdf_file, "rb") as f:
        st.download_button("Download PDF", f, file_name=pdf_file)
