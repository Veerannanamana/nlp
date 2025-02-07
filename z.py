import streamlit as st
import speech_recognition as sr
import pyttsx3

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen to user's speech and convert it to text."""
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            st.write(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            return "Sorry, I didn't catch that. Please try again."
        except sr.RequestError:
            return "Sorry, there was an issue with the speech recognition service."

def calculate(expression):
    """Evaluate a mathematical expression after replacing spoken words with symbols."""
    # Replace spoken words with mathematical symbols
    expression = expression.replace("plus", "+")
    expression = expression.replace("minus", "-")
    expression = expression.replace("into", "*")
    expression = expression.replace("divide", "/")
    expression = expression.replace("cap", "**")
    
    try:
        result = eval(expression)  # Use eval to calculate the result
        return result
    except Exception as e:
        return f"Error: {e}"

def main():
    st.title("Voice-Enabled Calculator")
    
    # Instructions for the user
    st.write("""
    **How to use the Voice-Enabled Calculator:**
    1. Click the 'Start Listening' button to begin.
    2. Speak your mathematical expression clearly.
    3. Use the following words for operations:
       - **Addition**: Say "plus" (e.g., "5 plus 3")
       - **Subtraction**: Say "minus" (e.g., "10 minus 4")
       - **Multiplication**: Say "into" (e.g., "6 into 2")
       - **Division**: Say "divide" (e.g., "8 divide 2")
       - **Exponentiation**: Say "cap" (e.g., "2 cap 3" for 2^3)
    4. The calculator will process your input and speak the result.
    5. After the result is spoken, the app will automatically listen for the next input.
    6. To stop the app, click the 'Stop Listening' button.
    """)
    
    # Use session state to manage the listening state
    if "listening" not in st.session_state:
        st.session_state.listening = False

    # Start/Stop Listening buttons
    if st.button("Start Listening"):
        st.session_state.listening = True

    if st.button("Stop Listening"):
        st.session_state.listening = False
        st.write("Listening stopped. Click 'Start Listening' to begin again.")

    # Continuous listening loop
    if st.session_state.listening:
        while st.session_state.listening:
            # Listen to the user's speech
            user_input = listen()
            
            if user_input:
                # Display the recognized text
                st.write(f"Recognized Input: {user_input}")
                
                # Calculate the result
                result = calculate(user_input)
                st.write(f"Result: {result}")
                
                # Speak the result
                speak(str(result))

                # Add a small delay to avoid rapid looping
                st.experimental_rerun()

if __name__ == "__main__":
    main()