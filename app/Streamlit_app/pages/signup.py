import sys
from pathlib import Path
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[3]

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from supabase_utils.auth import signup

from supabase_utils.validation import (
    validate_email,
    validate_password
)

st.title("Create Account")

email = st.text_input(
    "Email"
)

password = st.text_input(
    "Password",
    type="password"
)

st.caption(
    """
Password must contain:

• Minimum 8 characters
• One uppercase letter
• One lowercase letter
• One number
• One special character
"""
)

if st.button("Signup"):

    if not validate_email(email):

        st.error(
            "Please enter a valid email address."
        )

        st.stop()

    if not validate_password(password):

        st.error(
            """
Password must contain:

• Minimum 8 characters
• One uppercase letter
• One lowercase letter
• One number
• One special character
"""
        )

        st.stop()

    try:

        signup(
            email,
            password
        )

        st.success(
            "Account created successfully."
        )

        st.switch_page(
            "pages/login.py"
        )

    except Exception as e:

        st.error(
            str(e)
        )