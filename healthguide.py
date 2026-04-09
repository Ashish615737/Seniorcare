import streamlit as st
import google.generativeai as genai
from apikey import gemini_api_key
from streamlit_lottie import st_lottie
import requests
import json

# Configure page
st.set_page_config(
    page_title="AI Health Guide",
    page_icon="🏥",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border-radius: 20px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .results-container {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-top: 2rem;
    }
    .section-header {
        color: #2c3e50;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #4CAF50;
    }
    .stTextInput > div > div > input {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 10px 15px;
        font-size: 1.1rem;
    }
    </style>
    """, unsafe_allow_html=True)


def load_lottie_url(url: str):
    """Load Lottie animation from URL"""
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None


def configure_gemini():
    """Configure Gemini AI"""
    genai.configure(api_key=gemini_api_key)
    return genai.GenerativeModel('gemini-pro')


def generate_health_guide(topic):
    """Generate structured health guide prompt"""
    return f"""
    Please provide a comprehensive health guide for {topic} with the following structure:

    Overview:
    - Brief description of {topic}
    - Common symptoms

    Causes:
    - List the main factors that can cause or contribute to {topic}

    Treatment Approaches:

    1. Ayurvedic Remedies:
    - Traditional ayurvedic treatments
    - Herbal remedies
    - Lifestyle modifications according to Ayurveda

    2. Modern Medical Treatments:
    - Current medical approaches
    - Available medications
    - Professional medical interventions

    Prevention:
    - Lifestyle changes
    - Dietary recommendations
    - Preventive measures

    When to Seek Medical Help:
    - Warning signs
    - Emergency symptoms

    Please provide detailed yet concise information for each section.
    """


def format_response(response_text):
    """Format the response text with proper styling"""
    sections = response_text.split('\n\n')
    formatted_text = ""

    for section in sections:
        if ':' in section.split('\n')[0]:
            section_title = section.split('\n')[0].strip()
            section_content = '\n'.join(section.split('\n')[1:])
            formatted_text += f"<div class='section-header'>{section_title}</div>\n{section_content}\n\n"
        else:
            formatted_text += section + "\n\n"

    return formatted_text


def main():
    # Initialize Gemini
    model = configure_gemini()

    # Load Lottie animation
    lottie_url = "https://assets1.lottiefiles.com/packages/lf20_5njp3vgg.json"
    lottie_health = load_lottie_url(lottie_url)

    # Header section with Lottie
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("<div class='main-header'>", unsafe_allow_html=True)
        st.title("🏥 AI Health Guide")
        st.markdown("Get comprehensive information about health conditions using AI")
        st.markdown("</div>", unsafe_allow_html=True)

    with col1:
        if lottie_health:
            st_lottie(lottie_health, height=200, key="health_animation")

    # Search section
    st.markdown("### 🔍 Search Health Condition")
    prompt = st.text_input(
        "",
        placeholder="Enter a health condition or symptom...",
        help="Type any health condition or symptom you want to learn about"
    )

    # Generate and display response
    if prompt:
        try:
            with st.spinner("🤔 Analyzing and gathering information..."):
                # Generate the complete prompt
                full_prompt = generate_health_guide(prompt)

                # Get response from Gemini
                response = model.generate_content(full_prompt)

                # Format and display the response
                st.markdown("<div class='results-container'>", unsafe_allow_html=True)
                formatted_response = format_response(response.text)
                st.markdown(formatted_response, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

                # Disclaimer
                st.markdown("""
                    ---
                    *Disclaimer: This information is generated by AI for educational purposes only. 
                    Always consult with healthcare professionals for medical advice.*
                    """)

        except Exception as e:
            st.error("😕 Oops! Something went wrong. Please try again.")
            st.exception(e)


if __name__ == "__main__":
    main()