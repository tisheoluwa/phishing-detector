import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib

# === Step 1: Load dataset ===
print("✅ Loading dataset...")
data = pd.read_csv('data/phishing_email.csv')  # Adjust path if inside /data folder

# === Step 2: Clean dataset ===
print("🔍 Cleaning data...")

# Drop rows with missing text or label
data = data.dropna(subset=['text_combined', 'label'])

# Convert label to numeric and remove invalid entries
data['label'] = pd.to_numeric(data['label'], errors='coerce')
data = data.dropna(subset=['label'])
data['label'] = data['label'].astype(int)

print(f"✅ Cleaned data. Rows remaining: {len(data)}")

# === Step 3: Feature extraction (TF-IDF) ===
print("🔧 Vectorizing text...")
texts = data['text_combined']
labels = data['label']

vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X = vectorizer.fit_transform(texts)
y = labels

# === Step 4: Split the data ===
print("📊 Splitting into training and test sets...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# === Step 5: Train the model ===
print("🤖 Training Logistic Regression model...")
model = LogisticRegression()
model.fit(X_train, y_train)

# === Step 6: Evaluate the model ===
print("📈 Evaluating model...")
y_pred = model.predict(X_test)
print("\n🔹 Classification Report:")
print(classification_report(y_test, y_pred))

# === Step 7: Save the model and vectorizer ===
print("💾 Saving model and vectorizer...")
joblib.dump(model, 'model/phishing_model.pkl')
joblib.dump(vectorizer, 'model/vectorizer.pkl')

print("\n✅ Done! Model and vectorizer saved.")
