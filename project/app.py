import streamlit as st
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from heapq import nlargest
from collections import defaultdict
import PyPDF2
from docx import Document
# Initialize NLTK
import nltk
nltk.download('punkt')
nltk.download('stopwords')

st.title("Text Summarization System")

# Sidebar for options
with st.sidebar:
    st.header("Settings")
    summary_length = st.slider(
        "Select summary length (sentences)", 
        min_value=1, 
        max_value=10, 
        value=3,
        help="Choose how many sentences you want in your summary"
    )
    method = st.radio(
        "Summarization Method",
        ["Extractive", "Abstractive"],
        help="Extractive takes key sentences from the text. Abstractive generates new sentences (more advanced)."
    )

# Text input area
input_text = st.text_area("Enter your text here:", height=200)

# File uploader
uploaded_file = st.file_uploader("Or upload a file", type=["txt", "pdf", "docx"])

def extract_text_from_file(uploaded_file):
    """Extract text from uploaded file"""
    if uploaded_file is None:
        return ""
    
    file_type = uploaded_file.name.split('.')[-1].lower()
    
    if file_type == 'pdf':
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        return " ".join([page.extract_text() for page in pdf_reader.pages])
            
    elif file_type == 'docx':
        doc = Document(uploaded_file)
        return "\n".join([para.text for para in doc.paragraphs])
            
    else:  # txt file
        return uploaded_file.getvalue().decode("utf-8")

def extractive_summarize(text, num_sentences):
    """Basic extractive summarization using NLTK"""
    sentences = sent_tokenize(text)
    
    if len(sentences) <= num_sentences:
        return " ".join(sentences) + "\n\n[Note: Original text is already short enough]"
    
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    words = [word for word in words if word.isalnum() and word not in stop_words]
    
    freq = FreqDist(words)
    ranking = defaultdict(int)
    
    for i, sentence in enumerate(sentences):
        for word in word_tokenize(sentence.lower()):
            if word in freq:
                ranking[i] += freq[word]
    
    top_sentences = nlargest(num_sentences, ranking, key=ranking.get)
    return " ".join([sentences[j] for j in sorted(top_sentences)])

def abstractive_summarize(text, num_sentences):
    """Placeholder for abstractive summarization"""
    st.warning("Abstractive summarization requires more advanced models. Using extractive method instead.")
    return extractive_summarize(text, num_sentences)

# Process when user clicks the summarize button
if st.button("Generate Summary"):
    if uploaded_file is not None:
        input_text = extract_text_from_file(uploaded_file)
    
    if not input_text.strip():
        st.error("Please enter text or upload a file")
    else:
        with st.spinner(f"Generating {summary_length}-sentence summary..."):
            # Display summary length above the summary
            st.subheader(f"Summary ({summary_length} {'sentence' if summary_length == 1 else 'sentences'})")
            
            if method == "Extractive":
                summary = extractive_summarize(input_text, summary_length)
            else:
                summary = abstractive_summarize(input_text, summary_length)
            
            # Display summary in a box with copy button
            st.text_area("Summary", summary, height=200, key="summary_output")
            
            # Download buttons
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="Download as TXT",
                    data=summary,
                    file_name="summary.txt",
                    mime="text/plain"
                )
            with col2:
                if st.button("Copy to Clipboard"):
                    st.session_state.summary_output = summary
                    st.success("Summary copied to clipboard!")