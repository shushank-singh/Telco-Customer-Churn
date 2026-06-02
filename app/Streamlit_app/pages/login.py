import sys
from pathlib import Path
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[3]

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from supabase_utils.auth import login

from supabase_utils.validation import (
    validate_email
)

st.title("Login")

email = st.text_input(
    "Email"
)

password = st.text_input(
    "Password",
    type="password"
)

if st.button("Login"):

    if not validate_email(email):

        st.error(
            "Please enter a valid email address."
        )

        st.stop()

    try:

        response = login(
            email,
            password
        )

        if response.user:

            st.session_state[
                "authenticated"
            ] = True

            st.session_state[
                "user_email"
            ] = response.user.email

            st.switch_page(
                "pages/dashboard.py"
            )

    except Exception:

        st.error(
            "Invalid email or password."
        )

st.divider()

if st.button(
    "Create New Account"
):

    st.switch_page(
        "pages/signup.py"
    )