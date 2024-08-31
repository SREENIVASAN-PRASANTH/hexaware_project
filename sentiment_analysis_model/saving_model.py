import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report, accuracy_score
from sklearn.linear_model import LogisticRegression

# Load the CSV files
train_data = pd.read_csv('D:/python projects/hexaware project/sentiment_analysis_model/train.csv', encoding='ISO-8859-1')
test_data = pd.read_csv('D:/python projects/hexaware project/sentiment_analysis_model/test.csv', encoding='ISO-8859-1')

# Drop rows with missing values in the 'text' column
train_data_cleaned = train_data.dropna(subset=['text'])
test_data_cleaned = test_data.dropna(subset=['text'])

# Extract features and labels from the cleaned training dataset
X_train = train_data_cleaned['text']
y_train = train_data_cleaned['sentiment']

# Extract features from the cleaned test dataset
X_test = test_data_cleaned['text']
y_test = test_data_cleaned['sentiment']

# Split the cleaned training data for validation
X_train_split, X_val_split, y_train_split, y_val_split = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words='english')

# Create a pipeline with TfidfVectorizer and MultinomialNB classifier
model = make_pipeline(vectorizer, LogisticRegression())

# Train the model on the training split
model.fit(X_train_split, y_train_split)

# # Predict the sentiment for the validation and test data
# y_val_pred = model.predict(X_val_split)
# y_test_pred = model.predict(X_test)

# # Evaluate the model performance
# val_accuracy = accuracy_score(y_val_split, y_val_pred)
# test_accuracy = accuracy_score(y_test, y_test_pred)

# print(f"Validation Accuracy: {val_accuracy}")
# print(f"Test Accuracy: {test_accuracy}")

# print("Validation Classification Report:")
# print(classification_report(y_val_split, y_val_pred))

# print("Test Classification Report:")
# print(classification_report(y_test, y_test_pred))


joblib.dump(model, "sentiment_model.pkl")

