import pickle

from django.conf import settings
from sklearn.metrics import f1_score,recall_score,accuracy_score,precision_score,confusion_matrix,classification_report
from sklearn.model_selection import train_test_split

import os
import re
import numpy as np
import keras
import math
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import nltk

from nltk.corpus import stopwords


def remove_tags(str):
    result = re.sub('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});','',str)          #remove HTML tags
    result = re.sub('https://.*','',result)   #remove URLs
    result = re.sub('[^0-9a-zA-Z\s]+','',result)     #remove non-alphanumeric characters 
    result = result.lower()
    return result

w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
lemmatizer = nltk.stem.WordNetLemmatizer()
def lemmatize_text(text):
    st = ""
    for w in w_tokenizer.tokenize(text):
        st = st + lemmatizer.lemmatize(w) + " "
    return st

def sentiment_accuracy_measures(y_test,predictions,avg_method):
    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions, average=avg_method)
    recall = recall_score(y_test, predictions, average=avg_method)
    f1score = f1_score(y_test, predictions, average=avg_method)
    target_names = ['0','1']
    print("Classification report")
    print("---------------------","\n")
    print(classification_report(y_test, predictions,target_names=target_names),"\n")
    print("Confusion Matrix")
    print("---------------------","\n")
    print(confusion_matrix(y_test, predictions),"\n")

    print("Accuracy Measures")
    print("---------------------","\n")
    print("Accuracy: ", accuracy)
    print("Precision: ", precision)
    print("Recall: ", recall)
    print("F1 Score: ", f1score)

    return accuracy,precision,recall,f1score
    
def sentiment_model_train(): 
    try: 
        print("Download stop words...")
        nltk.download('stopwords')

        print("Load dataset...")
        data = pd.read_csv(os.path.join(settings.BASE_DIR, 'Spamchan/static/sentiment_analysis_train_dataset.csv'))

        print("Preprocessing...")
        data['review']=data['review'].apply(lambda cw : remove_tags(cw))
        stop_words = set(stopwords.words('english'))
        data['review'] = data['review'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop_words)]))
        data['review'] = data.review.apply(lemmatize_text)

        print("Embedding...")
        reviews = data['review'].values
        labels = data['sentiment'].values

        encoder = LabelEncoder()
        encoded_labels = encoder.fit_transform(labels)

        train_sentences, test_sentences, train_labels, test_labels = train_test_split(reviews, encoded_labels, stratify = encoded_labels)

        vocab_size = 3000 # choose based on statistics
        oov_tok = ''
        embedding_dim = 100
        max_length = 200 # choose based on statistics, for example 150 to 200

        tokenizer = Tokenizer(num_words = vocab_size, oov_token=oov_tok)
        tokenizer.fit_on_texts(train_sentences)

        train_sequences = tokenizer.texts_to_sequences(train_sentences)
        train_padded = pad_sequences(train_sequences, padding='post', maxlen=max_length)

        print("Building model...")
        sentiment_model = keras.Sequential([
            keras.layers.Embedding(vocab_size, embedding_dim, input_shape=(max_length,)),
            keras.layers.Bidirectional(keras.layers.LSTM(64)),
            keras.layers.Dense(24, activation='relu'),
            keras.layers.Dense(1, activation='sigmoid')
        ])

        print("Compling model...")
        sentiment_model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])

        print("Training...")
        num_epochs = 5
        sentiment_model.fit(train_padded, train_labels, epochs=num_epochs, verbose=1, validation_split=0.1)

        with open('sentiment_model.pkl', 'wb') as f:
            pickle.dump(sentiment_model.get_weights(), f)

        print("Successfully trained sentiment model!")

    except Exception as e: 
        print(getattr(e, "message", repr(e)))
