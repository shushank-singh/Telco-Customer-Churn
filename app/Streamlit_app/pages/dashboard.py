import streamlit as st
import requests
import plotly.graph_objects as go
from supabase_utils.database import (
    save_prediction
)


st.set_page_config(
    page_title="Telco Customer Churn Dashboard",
    page_icon="📡",
    layout="wide"
)


if not st.session_state.get(
    "authenticated",
    False
):

    st.switch_page(
        "pages/login.py"
    )

with st.sidebar:

    st.success(
        f"👤 {st.session_state.get('user_email')}"
    )

    if st.button(
        "📜 Prediction History"
    ):

        st.switch_page(
            "pages/history.py"
        )

    if st.button("Logout"):

        st.session_state.clear()

        st.switch_page(
            "pages/login.py"
        )


st.title("📡 Telco Customer Churn Prediction Dashboard")

st.markdown(
    """
    Predict whether a telecom customer is likely to churn or stay 🚀
    """
)

st.markdown("---")


st.sidebar.title("⚙️ Dashboard Settings")

show_json = st.sidebar.checkbox(
    "Show API Response JSON",
    value=False
)

show_probability = st.sidebar.checkbox(
    "Show Confidence Score",
    value=True
)


# =========================
# CUSTOMER PROFILE
# =========================

with st.expander(
    "👤 Customer Profile",
    expanded=True
):

    col1, col2 = st.columns(2)

    with col1:
        gender = st.selectbox(
            "Gender",
            ["Male", "Female"]
        )

        partner = st.selectbox(
            "Partner",
            ["Yes", "No"]
        )

    with col2:
        senior = st.selectbox(
            "Senior Citizen",
            [0, 1]
        )

        dependents = st.selectbox(
            "Dependents",
            ["Yes", "No"]
        )

    tenure = st.slider(
        "Customer Tenure (Months)",
        0,
        72,
        12
    )


# =========================
# TELECOM SERVICES
# =========================

with st.expander(
    "📞 Telecom Services",
    expanded=False
):

    col1, col2 = st.columns(2)

    with col1:

        phone_service = st.selectbox(
            "Phone Service",
            ["Yes", "No"]
        )

        internet_service = st.selectbox(
            "Internet Service",
            ["DSL", "Fiber optic", "No"]
        )

        if internet_service == "No":

            online_security = "No internet service"

            st.selectbox(
                "Online Security",
                ["No internet service"],
                disabled=True
            )

        else:

            online_security = st.selectbox(
                "Online Security",
                ["Yes", "No"]
            )

    with col2:

        multiple_lines = st.selectbox(
            "Multiple Lines",
            ["Yes", "No", "No phone service"]
        )

        if internet_service == "No":

            online_backup = "No internet service"

            st.selectbox(
                "Online Backup",
                ["No internet service"],
                disabled=True
            )

        else:

            online_backup = st.selectbox(
                "Online Backup",
                ["Yes", "No"]
            )

    if internet_service == "No":

        device_protection = "No internet service"

        st.selectbox(
            "Device Protection",
            ["No internet service"],
            disabled=True
        )

    else:

        device_protection = st.selectbox(
            "Device Protection",
            ["Yes", "No"]
        )


# =========================
# BILLING & SUPPORT
# =========================

with st.expander(
    "💳 Billing & Support",
    expanded=False
):

    col1, col2 = st.columns(2)

    with col1:

        if internet_service == "No":

            tech_support = "No internet service"

            st.selectbox(
                "Tech Support",
                ["No internet service"],
                disabled=True
            )

        else:

            tech_support = st.selectbox(
                "Tech Support",
                ["Yes", "No"]
            )

        streaming_movies = (
            "No internet service"
            if internet_service == "No"
            else st.selectbox(
                "Streaming Movies",
                ["Yes", "No"]
            )
        )

        paperless = st.selectbox(
            "Paperless Billing",
            ["Yes", "No"]
        )

    with col2:

        if internet_service == "No":

            streaming_tv = "No internet service"

            st.selectbox(
                "Streaming TV",
                ["No internet service"],
                disabled=True
            )

        else:

            streaming_tv = st.selectbox(
                "Streaming TV",
                ["Yes", "No"]
            )

        contract = st.selectbox(
            "Contract Type",
            ["Month-to-month", "One year", "Two year"]
        )

        payment = st.selectbox(
            "Payment Method",
            [
                "Electronic check",
                "Mailed check",
                "Bank transfer (automatic)",
                "Credit card (automatic)"
            ]
        )

    monthly_charges = st.slider(
        "Monthly Charges",
        0.0,
        150.0,
        75.0
    )

    total_charges = round(
        monthly_charges * tenure,
        2
    )

    st.metric(
        "💰 Calculated Total Charges",
        f"₹{total_charges:,.2f}"
    )


st.markdown("---")


if st.button(
    "🚀 Predict Customer Churn",
    use_container_width=True
):

    payload = {
        "gender": gender,
        "SeniorCitizen": senior,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "PhoneService": phone_service,
        "MultipleLines": multiple_lines,
        "InternetService": internet_service,
        "OnlineSecurity": online_security,
        "OnlineBackup": online_backup,
        "DeviceProtection": device_protection,
        "TechSupport": tech_support,
        "StreamingTV": streaming_tv,
        "StreamingMovies": streaming_movies,
        "Contract": contract,
        "PaperlessBilling": paperless,
        "PaymentMethod": payment,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges
    }

    api_url = "https://telco-customer-churn-ysfb.onrender.com/predict"

    with st.spinner("🤖 AI Model is analyzing customer data..."):

        try:

            response = requests.post(
                api_url,
                json=payload
            )

            if response.status_code == 200:

                result = response.json()

                prediction = result["Prediction"]
                confidence = float(result["Confidence"])
                risk = result["RiskLevel"]

                save_prediction(

                    user_id=st.session_state["user_id"],

                    customer_data=payload,

                    prediction=prediction,

                    confidence=confidence
                )

                risk_factors = []
                positive_factors = []


                if contract == "Month-to-month":
                    risk_factors.append("Month-to-Month Contract")

                if payment == "Electronic check":
                    risk_factors.append("Electronic Check Payment")

                if tenure < 12:
                    risk_factors.append("Short Customer Tenure")

                if monthly_charges > 70:
                    risk_factors.append("High Monthly Charges")

                if tech_support == "No":
                    risk_factors.append("No Tech Support")

                if online_security == "No":
                    risk_factors.append("No Online Security")


                if contract in ["One year", "Two year"]:
                    positive_factors.append("Long-Term Contract")

                if tenure > 24:
                    positive_factors.append("Long Customer Relationship")

                if tech_support == "Yes":
                    positive_factors.append("Tech Support Enabled")

                if online_security == "Yes":
                    positive_factors.append("Online Security Enabled")

                if monthly_charges < 70:
                    positive_factors.append("Affordable Monthly Charges")



                st.markdown("---")

                if prediction == "Customer Will Churn":

                    st.error(
                        f"⚠️ Prediction: {prediction}"
                    )

                else:

                    st.success(
                        f"✅ Prediction: {prediction}"
                    )


                metric1, metric2, metric3 = st.columns(3)

                with metric1:
                    st.metric(
                        "📊 Churn Score",
                        f"{confidence:.1f}%"
                    )

                with metric2:
                    st.metric(
                        "🔥 Risk Level",
                        risk
                    )

                with metric3:
                    st.metric(
                        "📅 Tenure",
                        f"{tenure} Months"
                    )


                st.subheader("📊 Churn Probability")

                gauge = go.Figure(
                    go.Indicator(
                        mode="gauge+number",
                        value=confidence,
                        title={
                            "text": "Churn Risk Score"
                        },
                        gauge={
                            "axis": {
                                "range": [0, 100]
                            },
                            "bar": {
                                "color": "#1f77b4"
                            },
                            "steps": [
                                {
                                    "range": [0, 40],
                                    "color": "green"
                                },
                                {
                                    "range": [40, 70],
                                    "color": "orange"
                                },
                                {
                                    "range": [70, 100],
                                    "color": "red"
                                }
                            ]
                        }
                    )
                )

                gauge.update_layout(
                    height=250,
                    margin=dict(
                        l=20,
                        r=20,
                        t=50,
                        b=20
                    )
                )

                st.plotly_chart(
                    gauge,
                    use_container_width=True
                )                


                st.subheader("🧠 AI Risk Analysis")

                if risk == "High Risk":

                    st.warning(
                        """
                        Customer shows strong churn behavior.

                        Reasons may include:
                        - Month-to-month contract
                        - Low tenure
                        - High monthly charges
                        - Lack of tech support
                        """
                    )

                elif risk == "Medium Risk":

                    st.info(
                        """
                        Customer has moderate churn probability.
                        Retention offers may help.
                        """
                    )

                else:

                    st.success(
                        """
                        Customer appears loyal and stable ✅
                        """
                    )

                if prediction == "Customer Will Churn":

                    st.subheader("⚠️ Risk Factors")

                    if risk_factors:

                        for factor in risk_factors:
                            st.warning(f"⚠️ {factor}")

                    else:

                        st.info(
                            "Model identified churn risk, but no major business-rule risk factors were detected."
                        )

                else:

                    st.subheader("✅ Positive Factors")

                    if positive_factors:

                        for factor in positive_factors:
                            st.success(f"✅ {factor}")

                    else:

                        st.info(
                            "Customer shows stable behavior patterns."
                        )


                if show_json:

                    st.subheader("📦 API Response JSON")
                    st.json(result)

            else:

                st.warning(
                    """
                    ⚠️ Unable to generate prediction.

                    Please review the entered customer information.
                    """
                )

        except Exception:

            st.error(
                """
                🚨 Service temporarily unavailable.

                Please try again in a few moments.
                """
            )