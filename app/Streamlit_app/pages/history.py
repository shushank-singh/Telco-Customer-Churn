import sys
from pathlib import Path
import streamlit as st
from supabase_utils.database import (
    get_user_predictions
)



ROOT_DIR = Path(__file__).resolve().parents[3]

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))


if not st.session_state.get(
    "authenticated",
    False
):

    st.switch_page(
        "pages/login.py"
    )


st.title(
    "📜 Prediction History"
)


user_id = st.session_state[
    "user_id"
]

data = get_user_predictions(
    user_id
)


if not data:

    st.info(
        "No prediction history found."
    )

else:

    st.dataframe(
        data,
        use_container_width=True
    )

if st.button(
    "⬅️ Back to Dashboard"
):

    st.switch_page(
        "pages/dashboard.py"
    )