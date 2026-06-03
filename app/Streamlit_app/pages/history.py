import sys
from pathlib import Path
import streamlit as st
import pandas as pd
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

    st.stop()

df = pd.DataFrame(data)

total_predictions = len(df)

churn_predictions = len(
    df[
        df["prediction"]
        ==
        "Customer Will Churn"
    ]
)

safe_predictions = (
    total_predictions
    -
    churn_predictions
)


col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "📊 Total Predictions",
        total_predictions
    )

with col2:

    st.metric(
        "⚠️ Churn Predictions",
        churn_predictions
    )

with col3:

    st.metric(
        "✅ Safe Predictions",
        safe_predictions
    )

st.markdown("---")

display_df = df[
    [
        "prediction",
        "confidence",
        "created_at"
    ]
].copy()

display_df.columns = [
    "Prediction",
    "Confidence (%)",
    "Created At"
]

st.dataframe(
    display_df,
    use_container_width=True
)

csv = display_df.to_csv(
    index=False
)

st.download_button(

    label="📥 Download History CSV",

    data=csv,

    file_name="prediction_history.csv",

    mime="text/csv"
)

if st.button(
    "⬅️ Back to Dashboard"
):

    st.switch_page(
        "pages/dashboard.py"
    )