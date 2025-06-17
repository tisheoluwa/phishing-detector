🛡️ Phishing Email Detection using NLP
This web app allows users to detect whether an email message is phishing or legitimate using a Natural Language Processing (NLP) model trained on real-world data.

✅ Features
🔍 Text or file-based prediction
Paste email content or upload .txt files for instant phishing detection.

👤 User-specific logging
Each user’s predictions are saved securely to individual logs.

📋 Admin dashboard
Password-protected view of all user predictions with filtering and a pie chart overview.

⬇️ Downloadable logs
Users and admins can download CSV logs of predictions.

🚀 How It Works
Text is preprocessed and transformed using TF-IDF

A trained Logistic Regression model predicts phishing likelihood

Confidence scores and results are displayed instantly

Results are logged to logs/<username>_log.csv

📦 Built With
Python · Streamlit · Scikit-learn · Pandas

TF-IDF · Logistic Regression · Altair for visualization

