import PyPDF2
from docx import Document
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize, sent_tokenize
def extract_text_from_file(file):
    """Extract text from PDF/DOCX/TXT files"""
    if file.type == "application/pdf":
        reader = PyPDF2.PdfReader(file)
        return " ".join([page.extract_text() for page in reader.pages])
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    else:  # TXT
        return file.getvalue().decode("utf-8")

def preprocess_text(text):
    """Clean and tokenize text"""
    stop_words = set(stopwords.words("english"))
    words = [word.lower() for word in word_tokenize(text) if word.isalnum()]
    return [word for word in words if word not in stop_words]

def extractive_summarize(text, n_sentences=3):
    """Extract top sentences using NLTK"""
    sentences = sent_tokenize(text)
    if len(sentences) <= n_sentences:
        return text
    word_freq = FreqDist(preprocess_text(text))
    ranking = {i: sum(word_freq[word] for word in preprocess_text(sentence))
               for i, sentence in enumerate(sentences)}
    top_indices = sorted(ranking, key=ranking.get, reverse=True)[:n_sentences]
    return " ".join([sentences[i] for i in sorted(top_indices)])
