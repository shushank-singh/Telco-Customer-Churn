import streamlit as st
import requests


st.set_page_config(
    page_title="Telco Customer Churn Dashboard",
    page_icon="📡",
    layout="wide"
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


col1, col2, col3 = st.columns(3)


with col1:

    st.subheader("👤 Customer Demographics")

    gender = st.selectbox(
        "Gender",
        ["Male", "Female"]
    )

    senior = st.selectbox(
        "Senior Citizen",
        [0, 1]
    )

    partner = st.selectbox(
        "Partner",
        ["Yes", "No"]
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


with col2:

    st.subheader("📞 Telecom Services")

    phone_service = st.selectbox(
        "Phone Service",
        ["Yes", "No"]
    )

    multiple_lines = st.selectbox(
        "Multiple Lines",
        ["Yes", "No", "No phone service"]
    )

    internet_service = st.selectbox(
        "Internet Service",
        ["DSL", "Fiber optic", "No"]
    )

    online_security = st.selectbox(
        "Online Security",
        ["Yes", "No", "No internet service"]
    )

    online_backup = st.selectbox(
        "Online Backup",
        ["Yes", "No", "No internet service"]
    )

    device_protection = st.selectbox(
        "Device Protection",
        ["Yes", "No", "No internet service"]
    )


with col3:

    st.subheader("💳 Billing & Support")

    tech_support = st.selectbox(
        "Tech Support",
        ["Yes", "No", "No internet service"]
    )

    streaming_tv = st.selectbox(
        "Streaming TV",
        ["Yes", "No", "No internet service"]
    )

    streaming_movies = st.selectbox(
        "Streaming Movies",
        ["Yes", "No", "No internet service"]
    )

    contract = st.selectbox(
        "Contract Type",
        ["Month-to-month", "One year", "Two year"]
    )

    paperless = st.selectbox(
        "Paperless Billing",
        ["Yes", "No"]
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

    total_charges = st.number_input(
        "Total Charges",
        min_value=0.0,
        value=900.0
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
                confidence = result["Confidence"]
                risk = result["RiskLevel"]


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
                        "🎯 Confidence",
                        f"{confidence}%"
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

                st.progress(min(int(confidence), 100))


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


                if show_json:

                    st.subheader("📦 API Response JSON")
                    st.json(result)

            else:

                st.error(
                    f"❌ API Error: {response.status_code}"
                )

                st.write(response.text)

        except Exception as e:

            st.error(f"REAL ERROR: {e}")


    