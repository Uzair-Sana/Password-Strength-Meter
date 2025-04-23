import streamlit as st
import re
import random
import plotly.graph_objects as go

# --- Password Check ---
def check_password_strength(password):
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters long.")

    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Use both uppercase and lowercase letters.")

    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Add at least one digit (0-9).")

    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("Include at least one special character (!@#$%^&*).")

    common_passwords = ["password", "123456", "qwerty", "password123", "admin"]
    if password.lower() in common_passwords:
        feedback.append("This password is too common.")
        score = min(score, 2)

    return score, feedback

# --- Password Generator ---
def generate_strong_password(length=12):
    if length < 8:
        length = 12
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
    password = [
        random.choice("abcdefghijklmnopqrstuvwxyz"),
        random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
        random.choice("0123456789"),
        random.choice("!@#$%^&*"),
    ]
    password += [random.choice(chars) for _ in range(length - 4)]
    random.shuffle(password)
    return ''.join(password)

# --- Gauge Chart ---
def plot_gauge(score):
    label_map = {
        0: "Very Weak",
        1: "Weak",
        2: "Weak",
        3: "Moderate",
        4: "Strong"
    }

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"Password Score: {label_map[score]}", 'font': {'size': 24}},
        gauge={
            'axis': {'range': [0, 4], 'tickwidth': 1, 'tickcolor': "darkgray"},
            'bar': {'color': "black"},
            'steps': [
                {'range': [0, 1], 'color': '#ff4b4b'},
                {'range': [1, 2], 'color': '#ffa94d'},
                {'range': [2, 3], 'color': '#ffe066'},
                {'range': [3, 4], 'color': '#a0e57c'},
                {'range': [4, 5], 'color': '#4caf50'}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))
    st.plotly_chart(fig)

# --- Streamlit UI ---
st.set_page_config(page_title="🔐 Password Strength Meter", layout="centered")
st.title("🔐 Password Strength Meter")

password = st.text_input("Enter your password", type="password")

if password:
    score, feedback = check_password_strength(password)

    st.subheader("📊 Visual Password Strength Meter")
    plot_gauge(score)

    if score == 4:
        st.success("✅ Strong Password!")
    elif score == 3:
        st.warning("⚠️ Moderate Password - Consider strengthening it.")
    else:
        st.error("❌ Weak Password - Needs improvement.")

    if feedback:
        st.subheader("Suggestions:")
        for tip in feedback:
            st.write("•", tip)

# --- Password Generator ---
st.markdown("---")
st.subheader("🔁 Need Help?")
if st.button("Generate Strong Password"):
    new_password = generate_strong_password()
    st.code(new_password, language="text")
