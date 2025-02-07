import streamlit as st
import speech_recognition as sr
import pyttsx3
import time

# Initialize the recognizer
recognizer = sr.Recognizer()

def speak(text):
    """Convert text to speech safely in Streamlit."""
    engine = pyttsx3.init()  # Initialize inside the function to avoid loop issues
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen to user's speech and convert it to text."""
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio).lower()
            st.write(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            return "Sorry, I didn't catch that. Please try again."
        except sr.RequestError:
            return "Sorry, there was an issue with the speech recognition service."

def calculate(expression):
    """Evaluate a mathematical expression after replacing spoken words with symbols."""
    expression = expression.replace("plus", "+")
    expression = expression.replace("minus", "-")
    expression = expression.replace("into", "*")
    expression = expression.replace("times", "*")
    expression = expression.replace("divide", "/")
    expression = expression.replace("cap", "**")
    
    try:
        result = eval(expression)  # Use eval to calculate the result
        return result
    except Exception as e:
        return f"Error: {e}"

def main():
    st.title("Voice-Enabled Calculator")
    
    st.write("""
    **How to use the Voice-Enabled Calculator:**
    - Click **"Start Listening"** to begin.
    - Click **"Stop Listening"** to pause calculations.
    - Speak your mathematical expression clearly.
    - Supported words:
        - **Addition**: "plus" (e.g., "5 plus 3")
        - **Subtraction**: "minus" (e.g., "10 minus 4")
        - **Multiplication**: "into" or "times" (e.g., "6 into 2")
        - **Division**: "divide" (e.g., "8 divide 2")
        - **Exponentiation**: "cap" (e.g., "2 cap 3" → 2³)
    - The result will be spoken aloud.
    - The app keeps listening until you stop it.
    """)

    # Initialize session state if not set
    if "listening" not in st.session_state:
        st.session_state.listening = False

    # Start and Stop buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Start Listening 🎤"):
            st.session_state.listening = True

    with col2:
        if st.button("Stop Listening ❌"):
            st.session_state.listening = False
            st.write("Listening paused. Click 'Start Listening' to resume.")

    # Main listening loop
    while st.session_state.listening:
        user_input = listen()
        
        if user_input:
            result = calculate(user_input)
            st.write(f"Result: {result}")
            speak(str(result))  # Speak the result
            
            time.sleep(2)  # Short delay before listening again (prevents too fast re-runs)
            st.experimental_rerun()  # Restart the loop for continuous calculations

if __name__ == "__main__":
    main()
