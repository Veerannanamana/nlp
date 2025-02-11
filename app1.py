import streamlit as st
import speech_recognition as sr
import pyttsx3
import time
import sympy as sp
from sympy.integrals.manualintegrate import integral_steps

# Initialize the recognizer
recognizer = sr.Recognizer()

def speak(text):
    """Convert text to speech safely in Streamlit."""
    engine = pyttsx3.init()
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
    
    # Handle implicit multiplication (e.g., "3x3" → "3*3")
    expression = expression.replace("x", "*")  # Replace 'x' with '*' for multiplication
    
    # Remove any non-numeric or non-operator characters (e.g., 's' in '1s')
    expression = ''.join([char for char in expression if char in '0123456789+-*/.() '])
    
    try:
        result = eval(expression)  # Use eval to calculate the result
        return round(result, 2) if isinstance(result, float) else result
    except Exception as e:
        return f"Error: Invalid Syntax"

def integrate_expression(expression):
    """Perform symbolic integration on the given expression and return steps."""
    try:
        x = sp.symbols('x')
        expr = sp.sympify(expression)  # Convert string to SymPy expression
        integral_result = sp.integrate(expr, x)
        
        # Get step-wise integration
        steps = integral_steps(expr, x)
        step_details = []
        while steps:
            step_details.append(f"Step {len(step_details) + 1}: {steps.__class__.__name__}")
            if hasattr(steps, 'substep'):
                steps = steps.substep
            else:
                break
        
        return f"∫ {expression} dx = {integral_result}", step_details
    except Exception as e:
        return f"Error: {str(e)}", None

def differentiate_expression(expression):
    """Perform symbolic differentiation."""
    try:
        x = sp.symbols('x')
        expr = sp.sympify(expression)  # Convert string to SymPy expression
        derivative_result = sp.diff(expr, x)
        return f"d/dx ({expression}) = {derivative_result}"
    except Exception as e:
        return f"Error: {str(e)}"

def trigonometry_operations(expression):
    """Perform trigonometric calculations."""
    try:
        x = sp.symbols('x')
        expr = sp.sympify(expression, evaluate=False)
        result = expr.evalf()
        return round(result, 2)
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.title("Voice-Enabled Calculator")

    # Custom CSS for styling
    st.markdown("""
    <style>
    .stTextArea textarea {
        background-color: #f0f2f6;
        color: #ff6347;
        font-size: 16px;
        border-radius: 10px;
        border: 2px solid #ff6347;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 12px;
        padding: 10px 24px;
        font-size: 16px;
        border: none;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    .stButton button:active {
        background-color: #3e8e41;
    }
    </style>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Basic Operations", "Mathematical Expressions", "Integration", "Differentiation", "Trigonometry"
    ])

    # Basic Operations
    with tab1:
        st.subheader("Basic Operations (Voice-Based)")

        st.write("""
        - Click **"Start Listening"** to begin.
        - Speak your mathematical expression clearly.
        - Example: "5 plus 3" → 8
        - The result will be spoken aloud.
        """)

        if "listening" not in st.session_state:
            st.session_state.listening = False

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Start Listening 🎤", key="start_listening"):
                st.session_state.listening = True

        with col2:
            if st.button("Stop Listening ❌", key="stop_listening"):
                st.session_state.listening = False
                st.write("Listening paused.")

        if st.session_state.listening:
            user_input = listen()
            
            if user_input:
                result = calculate(user_input)
                st.write(f"Result: {result}")
                speak(str(result))
                time.sleep(1)
                st.experimental_rerun()

    # Mathematical Expressions
    with tab2:
        st.subheader("Mathematical Expressions")

        st.write("""
        - Enter a mathematical expression in the text area below.
        - Example: (8 * 8 * 8) / 9
        - Click **"Calculate"** to evaluate the expression.
        - The result will be displayed and spoken aloud.
        """)

        expression = st.text_area("Enter a mathematical expression (e.g., (8 * 8 * 8) / 9)", key="math_expr")

        if st.button("Calculate", key="calculate"):
            if expression:
                result = calculate(expression)
                st.write(f"**Result:** {result}")
                speak(f"The result is {result}")
            else:
                st.warning("Please enter a valid mathematical expression.")

    # Integration Operations
    with tab3:
        st.subheader("Integration Operations")
        st.write("""
        - Enter an integration expression in the text area below.
        - Example: x**3 + x**3
        - Click **"Integrate"** to evaluate the expression.
        - The result and step-wise solution will be displayed.
        """)
        integral_expr = st.text_area("∫ Enter function to integrate (in terms of x)", key="integral_expr", height=100)
        if st.button("Integrate", key="integrate"):
            if integral_expr:
                result, steps = integrate_expression(integral_expr)
                st.write(f"**Result:** {result}")
                if steps:
                    st.write("**Step-wise Solution:**")
                    for step in steps:
                        st.write(step)
            else:
                st.warning("Please enter a valid function to integrate.")

    # Differentiation Operations
    with tab4:
        st.subheader("Differentiation Operations")
        st.write("""
        - Enter a differentiation expression in the text area below.
        - Example: x**2 + 3*x + 5
        - Click **"Differentiate"** to evaluate the expression.
        - The result will be displayed.
        """)
        diff_expr = st.text_area("d/dx Enter function to differentiate (in terms of x)", key="diff_expr", height=100)
        if st.button("Differentiate", key="differentiate"):
            if diff_expr:
                result = differentiate_expression(diff_expr)
                st.write(f"**Derivative:** {result}")
            else:
                st.warning("Please enter a valid function to differentiate.")

    # Trigonometry Operations
    with tab5:
        st.subheader("Trigonometry Operations")
        st.write("""
        - Enter a trigonometric expression in the text area below.
        - Example: sin(pi/4), cos(pi/3), tan(pi/6)
        - Click **"Evaluate Trigonometry"** to evaluate the expression.
        - The result will be displayed and spoken aloud.
        """)
        
        trigo_expr = st.text_area("Enter trigonometric function", key="trigo_expr", height=150)

        if st.button("Evaluate Trigonometry"):
            if trigo_expr:
                result = trigonometry_operations(trigo_expr)
                st.write(f"**Result:** {result}")
                speak(f"The result is {result}")

if __name__ == "__main__":
    main()