import streamlit as st

if st.session_state.get(
    "authenticated",
    False
):

    st.switch_page(
        "pages/dashboard.py"
    )

else:

    st.switch_page(
        "pages/login.py"
    )