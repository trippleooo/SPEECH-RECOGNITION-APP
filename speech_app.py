import streamlit as st
import speech_recognition as sr
import os

LANGUAGES = {
    "English (US)": "en-US",
    "French": "fr-FR",
    "Swahili": "sw-KE"
}

APIS = ["Google", "Sphinx"]

def transcribe_speech(api_choice, language):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Speak now...")
        try:
            audio_text = r.listen(source, timeout=5, phrase_time_limit=10)
            st.info("🔎 Transcribing...")

            if api_choice == "Google":
                return r.recognize_google(audio_text, language=language)
            elif api_choice == "Sphinx":
                return r.recognize_sphinx(audio_text, language=language)
            else:
                return "Unsupported API selected."
        except sr.WaitTimeoutError:
            return "No speech detected. Please try again."
        except sr.UnknownValueError:
            return "Sorry, I couldn’t understand you."
        except sr.RequestError as e:
            return f"API error: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"

def save_transcription(text):
    if text:
        with open("transcription.txt", "a") as f:
            f.write(text + "\n")
        st.success("Transcription saved to 'transcription.txt'.")

def main():
    st.set_page_config(page_title="Speech Recognition App", layout="centered")
    st.title("🗣️ Speech Recognition App")
    st.markdown("Speak and see your words converted into text!")

    language = st.selectbox("Select Language", list(LANGUAGES.keys()))
    lang_code = LANGUAGES[language]

    api_choice = st.radio("Choose Recognition API", APIS)

    if st.button("Start Recording"):
        text = transcribe_speech(api_choice, lang_code)
        st.write("**Transcription:**", text)

        if text and "Sorry" not in text:
            if st.checkbox("Save this transcription?"):
                save_transcription(text)

    if os.path.exists("transcription.txt"):
        with open("transcription.txt", "r") as f:
            st.text_area("Saved Transcriptions", f.read(), height=200)

if __name__ == "__main__":
    main()
