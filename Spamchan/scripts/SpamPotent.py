import pickle
from django.conf import settings
from sklearn.feature_extraction.text import TfidfVectorizer

feature_extraction = TfidfVectorizer(min_df=1, stop_words='english', lowercase=True)

def getProb(message):
    path = f"{settings.BASE_DIR}/SpamChan/pickle/spampot.pkl"
    vec_path = f"{settings.BASE_DIR}/SpamChan/pickle/vectorizer.pkl"
    with open(path, 'rb') as file:
        model = pickle.load(file)

    with open(vec_path, 'rb') as file:
        feature_extraction = pickle.load(file)

    input_data_features = feature_extraction.transform([message])
    prediction_proba = model.predict_proba(input_data_features)
    return f"{round(prediction_proba[0][0]*100, 2)}%"
