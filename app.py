import streamlit as st
import joblib
import os
import pandas as pd
import datetime
import altair as alt
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()
admin_password = os.getenv("ADMIN_PASSWORD")

# === Load model and vectorizer ===
model = joblib.load('model/phishing_model.pkl')
vectorizer = joblib.load('model/vectorizer.pkl')

# === Ensure log folder exists ===
if not os.path.exists('logs'):
    os.makedirs('logs')

# === Streamlit page config ===
st.set_page_config(page_title="Phishing Detector", layout="centered")
st.title("🛡️ Phishing Email Detector")
st.markdown("Use NLP to detect whether a message is **phishing** or **legitimate**.")

# === Tabs ===
tab1, tab2 = st.tabs(["🔍 Predict", "📋 View Logs"])

# === TAB 1: PREDICTION ===
with tab1:
    st.subheader("👤 Enter your username")
    username = st.text_input("Username (for saving your history):").strip()

    user_input = st.text_area("📩 Paste email content here:", height=200)

    uploaded_file = st.file_uploader("📎 Or upload a `.txt` file", type=['txt'])
    if uploaded_file is not None:
        file_text = uploaded_file.read().decode("utf-8")
        user_input = file_text
        st.info("📄 File content loaded successfully.")

    if st.button("🔍 Detect"):
        if username == "":
            st.warning("⚠️ Please enter a username.")
        elif user_input.strip() == "":
            st.warning("⚠️ Please paste or upload email content.")
        else:
            # Predict
            vectorized_input = vectorizer.transform([user_input])
            prediction = model.predict(vectorized_input)[0]
            prob = model.predict_proba(vectorized_input)[0]

            label = "Phishing" if prediction == 1 else "Legitimate"
            confidence = prob[prediction] * 100

            if prediction == 1:
                st.error(f"🚨 **Phishing Detected!** Confidence: {confidence:.2f}%")
            else:
                st.success(f"✅ **Safe Message.** Confidence: {confidence:.2f}%")

            # === Save to user's log ===
            log_file = f"logs/{username}_log.csv"
            new_log = pd.DataFrame([{
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "user": username,
                "input_preview": user_input[:100].replace('\n', ' ') + "...",
                "prediction": label,
                "confidence": f"{confidence:.2f}%"
            }])

            if os.path.exists(log_file):
                log_df = pd.read_csv(log_file)
                log_df = pd.concat([log_df, new_log], ignore_index=True)
            else:
                log_df = new_log

            log_df.to_csv(log_file, index=False)
            st.info(f"📝 Your result was saved to `{log_file}`")

# === TAB 2: VIEW LOGS ===
with tab2:
    st.subheader("🔐 Log Access")

    access_type = st.radio("Who are you?", ["User", "Admin"])

    if access_type == "User":
        view_user = st.text_input("Enter your username to view your logs:").strip()
        if view_user:
            user_log_file = f"logs/{view_user}_log.csv"
            if os.path.exists(user_log_file):
                logs = pd.read_csv(user_log_file)
                st.success(f"📄 Showing logs for: **{view_user}**")
                st.dataframe(logs, use_container_width=True)

                csv = logs.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="⬇️ Download Your Logs",
                    data=csv,
                    file_name=f'{view_user}_phishing_logs.csv',
                    mime='text/csv'
                )
            else:
                st.warning("⚠️ No log file found for that username.")

    elif access_type == "Admin":
        admin_pass = st.text_input("Enter admin password:", type="password")
        if admin_pass == admin_password:
            all_logs = []
            for file in os.listdir("logs"):
                if file.endswith("_log.csv"):
                    df = pd.read_csv(os.path.join("logs", file))
                    all_logs.append(df)
            if all_logs:
                full_df = pd.concat(all_logs, ignore_index=True)
                st.success("✅ Admin access granted.")
                st.subheader("📋 All Logs")
                st.dataframe(full_df, use_container_width=True)

                # Pie Chart
                st.subheader("📊 Prediction Breakdown")
                chart_data = full_df['prediction'].value_counts().reset_index()
                chart_data.columns = ['prediction', 'count']

                chart = alt.Chart(chart_data).mark_arc(innerRadius=50).encode(
                    theta=alt.Theta(field="count", type="quantitative"),
                    color=alt.Color(field="prediction", type="nominal"),
                    tooltip=["prediction", "count"]
                )

                st.altair_chart(chart, use_container_width=True)

                csv = full_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="⬇️ Download All Logs",
                    data=csv,
                    file_name='all_phishing_logs.csv',
                    mime='text/csv'
                )
            else:
                st.warning("No user logs found yet.")
        elif admin_pass:
            st.error("❌ Incorrect admin password.")
