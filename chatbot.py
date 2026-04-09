import time
import os
import streamlit as st
from streamlit_chat import message
import speech_recognition as sr
from gtts import gTTS
import tempfile
import google.generativeai as genai
from apikey import gemini_api_key
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ChatbotConfig:
    """Configuration class for the chatbot"""
    MODEL_NAME = 'gemini-pro'
    SUPPORTED_LANGUAGES = {
        "en": "English",
        "hi": "हिंदी",
        "te": "తెలుగు",
        "ta": "தமிழ்",
        "kn": "ಕನ್ನಡ",
        "ml": "മലയാളം"
    }


class VoiceHandler:
    """Handles voice input and output functionality"""

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def record_audio(self, language: str) -> Optional[str]:
        """Record and transcribe audio input"""
        try:
            with self.microphone as source:
                with st.spinner("🎤 Recording..."):
                    audio = self.recognizer.listen(source)

                with st.spinner("🔍 Processing speech..."):
                    text = self.recognizer.recognize_google(audio, language=language)
                    return text
        except sr.UnknownValueError:
            st.error("❌ Could not understand audio")
        except sr.RequestError as e:
            st.error(f"❌ Error with speech recognition service: {e}")
        return None

    @staticmethod
    def text_to_speech(text: str, language: str) -> Optional[str]:
        """Convert text to speech"""
        try:
            speech = gTTS(text=text, lang=language)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                temp_file_path = f.name
                speech.save(temp_file_path)
            return temp_file_path
        except Exception as e:
            logger.error(f"Error in text-to-speech conversion: {e}")
            return None


class GeminiChatbot:
    """Main chatbot application class"""

    def __init__(self):
        self.config = ChatbotConfig()
        self.voice_handler = VoiceHandler()
        self.setup_gemini()
        self.initialize_session_state()
        self.setup_ui()

    def setup_gemini(self):
        """Initialize Gemini API"""
        try:
            genai.configure(api_key=gemini_api_key)
            self.model = genai.GenerativeModel(self.config.MODEL_NAME)
        except Exception as e:
            logger.error(f"Failed to initialize Gemini: {e}")
            st.error("Failed to initialize AI model. Please check your API key.")
            st.stop()

    def initialize_session_state(self):
        """Initialize Streamlit session state variables"""
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        if 'chat' not in st.session_state:
            st.session_state.chat = None

    def setup_ui(self):
        """Set up the user interface"""
        st.set_page_config(
            page_title="AI Health Assistant",
            page_icon="🤖",
            layout="wide"
        )

        # Custom CSS for better styling
        st.markdown("""
            <style>
            .stButton > button {
                background-color: #4CAF50;
                color: white;
                border-radius: 20px;
                padding: 10px 20px;
            }
            .chat-message {
                padding: 1rem;
                border-radius: 0.5rem;
                margin-bottom: 1rem;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .stTextInput > div > div > input {
                background-color: #f0f2f6;
            }
            </style>
            """, unsafe_allow_html=True)

    def setup_sidebar(self):
        """Set up the simplified sidebar with language selection and clear chat button"""
        with st.sidebar:
            st.markdown("# ⚙️ Settings")
            st.divider()

            # Language selector
            selected_lang = st.selectbox(
                "🌐 Select Language",
                options=list(self.config.SUPPORTED_LANGUAGES.keys()),
                format_func=lambda x: self.config.SUPPORTED_LANGUAGES[x],
                key='language_selector'
            )

            # Clear chat button
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.messages = []
                st.session_state.chat = None
                st.experimental_rerun()

            return selected_lang

    def handle_user_input(self, language: str) -> Optional[str]:
        """Handle both text and voice input from user"""
        col1, col2 = st.columns([4, 1])

        with col1:
            text_input = st.text_input(
                "💭 Type your message...",
                key="user_text_input",
                placeholder="Ask me anything..."
            )

        with col2:
            voice_button = st.button("🎤 Speak", use_container_width=True)

        if voice_button:
            return self.voice_handler.record_audio(language)
        return text_input

    def process_response(self, response, language: str):
        """Process and display AI response"""
        with st.chat_message("assistant", avatar="🤖"):
            message_placeholder = st.empty()
            full_response = ""

            for chunk in response:
                for ch in chunk.text.split(" "):
                    full_response += ch + " "
                    time.sleep(0.05)
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

            # Generate audio response
            audio_file = self.voice_handler.text_to_speech(full_response, language)
            if audio_file:
                st.audio(audio_file, format="audio/mp3")
                os.remove(audio_file)

    def run(self):
        """Main application loop"""
        st.title("🤖 AI Health Assistant")
        st.markdown("Your personal health companion powered by Gemini AI")
        st.divider()

        # Setup sidebar and get selected language
        selected_language = self.setup_sidebar()

        # Get user input
        user_input = self.handle_user_input(selected_language)

        if user_input:
            # Display user message
            with st.chat_message("user", avatar="👤"):
                st.markdown(user_input)

            # Update session state
            st.session_state.messages.append({
                "role": "user",
                "content": user_input
            })

            # Initialize or get chat session
            if not st.session_state.chat:
                st.session_state.chat = self.model.start_chat()

            # Get AI response
            try:
                with st.spinner("🤔 Thinking..."):
                    response = st.session_state.chat.send_message(user_input, stream=True)
                    self.process_response(response, selected_language)

                # Update messages
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": st.session_state.chat.history[-1].parts[0].text,
                    "avatar": "🤖"
                })

            except Exception as e:
                logger.error(f"Error getting AI response: {e}")
                st.error("Failed to get response from AI. Please try again.")

        # Display chat history
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"], avatar=msg.get("avatar", "👤")):
                st.markdown(msg["content"])


if __name__ == "__main__":
    chatbot = GeminiChatbot()
    chatbot.run()