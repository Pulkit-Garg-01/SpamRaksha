import re
import numpy as np
import keras
import math
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
import nltk

nltk.download('stopwords')
from nltk.corpus import stopwords


# LOAD DATASET
data = pd.read_csv('IMDB Dataset.csv')


# PREPROCESSING
def remove_tags(str):
    result = re.sub('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});','',str)          #remove HTML tags
    result = re.sub('https://.*','',result)   #remove URLs
    result = re.sub('[^0-9a-zA-Z\s]+','',result)     #remove non-alphanumeric characters 
    result = result.lower()
    return result

# Remove tags
data['review']=data['review'].apply(lambda cw : remove_tags(cw))

# Remove stop words
stop_words = set(stopwords.words('english'))
data['review'] = data['review'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop_words)]))

# Tokenization
w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
lemmatizer = nltk.stem.WordNetLemmatizer()

def lemmatize_text(text, w_tokenizer, lemmatizer):
    st = ""
    for w in w_tokenizer.tokenize(text):
        st = st + lemmatizer.lemmatize(w) + " "
    return st
    
data['review'] = data.review.apply(lemmatize_text)


# EMBEDDING
reviews = data['review'].values
labels = data['sentiment'].values

encoder = LabelEncoder()
encoded_labels = encoder.fit_transform(labels)

train_sentences, test_sentences, train_labels, test_labels = train_test_split(reviews, encoded_labels, stratify = encoded_labels)

# Hyperparameters of the model
vocab_size = 3000 # choose based on statistics
oov_tok = ''
embedding_dim = 100
max_length = 200 # choose based on statistics, for example 150 to 200
padding_type='post'
trunc_type='post'

# tokenize sentences
tokenizer = Tokenizer(num_words = vocab_size, oov_token=oov_tok)
tokenizer.fit_on_texts(train_sentences)
word_index = tokenizer.word_index

# convert train dataset to sequence and pad sequences
train_sequences = tokenizer.texts_to_sequences(train_sentences)
train_padded = pad_sequences(train_sequences, padding='post', maxlen=max_length)

# convert Test dataset to sequence and pad sequences
test_sequences = tokenizer.texts_to_sequences(test_sentences)
test_padded = pad_sequences(test_sequences, padding='post', maxlen=max_length)


# MODEL BUILDING
# model initialization
sentiment_model = keras.Sequential([
    keras.layers.Embedding(vocab_size, embedding_dim, input_shape=(max_length,)),
    keras.layers.Bidirectional(keras.layers.LSTM(64)),
    keras.layers.Dense(24, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
])

# compile model
sentiment_model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])


# TRAINING
num_epochs = 5
history = sentiment_model.fit(train_padded, train_labels, epochs=num_epochs, verbose=1, validation_split=0.1)

# def train_sentiment_model():
#     # LOAD DATASET
#     data = pd.read_csv('IMDB Dataset.csv')

#     # Remove tags
#     data['review']=data['review'].apply(lambda cw : remove_tags(cw))

#     # Remove stop words
#     stop_words = set(stopwords.words('english'))
#     data['review'] = data['review'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop_words)]))

#     data['review'] = data.review.apply(lemmatize_text)

#     # EMBEDDING
#     reviews = data['review'].values
#     labels = data['sentiment'].values

#     encoder = LabelEncoder()
#     encoded_labels = encoder.fit_transform(labels)

#     train_sentences, test_sentences, train_labels, test_labels = train_test_split(reviews, encoded_labels, stratify = encoded_labels)

#     # Hyperparameters of the model
#     vocab_size = 3000 # choose based on statistics
#     oov_tok = ''
#     embedding_dim = 100
#     max_length = 200 # choose based on statistics, for example 150 to 200
#     padding_type='post'
#     trunc_type='post'

#     # tokenize sentences
#     tokenizer = Tokenizer(num_words = vocab_size, oov_token=oov_tok)
#     tokenizer.fit_on_texts(train_sentences)
#     word_index = tokenizer.word_index

#     # convert train dataset to sequence and pad sequences
#     train_sequences = tokenizer.texts_to_sequences(train_sentences)
#     train_padded = pad_sequences(train_sequences, padding='post', maxlen=max_length)

#     # convert Test dataset to sequence and pad sequences
#     test_sequences = tokenizer.texts_to_sequences(test_sentences)
#     test_padded = pad_sequences(test_sequences, padding='post', maxlen=max_length)

