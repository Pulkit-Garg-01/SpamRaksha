import pickle
import keras
import nltk
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status
from Spamchan.serializers import ReportSerializer
from Spamchan.models import Report, FraudulentUser, User, Company
from Spamchan.services import remove_tags, lemmatize_text
from tensorflow.keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
lemmatizer = nltk.stem.WordNetLemmatizer()

class ReportModelViewset(viewsets.ModelViewSet):
    serializer_class= ReportSerializer
    queryset= Report.objects.all()

    # def list(self, request, *args, **kwargs):
    #     report_message = remove_tags(report_message)
    #     report_message = lemmatize_text(report_message)
    #     report_message = [report_message]

    #     vocab_size = 3000 # choose based on statistics
    #     oov_tok = ''
    #     embedding_dim = 100
    #     max_length = 200

    #     tokenizer = Tokenizer(num_words = vocab_size, oov_token=oov_tok)
    #     tokenizer.fit_on_texts(report_message)

    #     report_sequences = tokenizer.texts_to_sequences(report_message)
    #     report_padded = pad_sequences(report_sequences, padding='post', maxlen=max_length)

    #     sentiment_model = keras.Sequential([
    #         keras.layers.Embedding(vocab_size, embedding_dim, input_shape=(max_length,)),
    #         keras.layers.Bidirectional(keras.layers.LSTM(64)),
    #         keras.layers.Dense(24, activation='relu'),
    #         keras.layers.Dense(1, activation='sigmoid')
    #     ])
    #     sentiment_model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])

    #     with open('sentiment_model.pkl', 'rb') as f:
    #         sentiment_model_weights = pickle.load(f)
    #         sentiment_model.set_weights(sentiment_model_weights)
        
    #     prediction = sentiment_model.predict(report_padded)

    #     return Response(prediction[0])

    def create(self, request, *args, **kwargs):
        report_message = request.data.get('message', None)
        company_id = request.data.get('reported_to', None)
        reporter_id = request.data.get('reporter', None)
        spammer_phno = request.data.get('spammer', None)

        report_message = "bad kill poison die"

        report_message = remove_tags(report_message)
        report_message = lemmatize_text(report_message)
        report_message = [report_message]

        vocab_size = 3000 # choose based on statistics
        oov_tok = ''
        embedding_dim = 100
        max_length = 200

        tokenizer = Tokenizer(num_words = vocab_size, oov_token=oov_tok)
        tokenizer.fit_on_texts(report_message)

        report_sequences = tokenizer.texts_to_sequences(report_message)
        report_padded = pad_sequences(report_sequences, padding='post', maxlen=max_length)

        sentiment_model = keras.Sequential([
            keras.layers.Embedding(vocab_size, embedding_dim, input_shape=(max_length,)),
            keras.layers.Bidirectional(keras.layers.LSTM(64)),
            keras.layers.Dense(24, activation='relu'),
            keras.layers.Dense(1, activation='sigmoid')
        ])
        sentiment_model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])

        with open('sentiment_model.pkl', 'rb') as f:
            sentiment_model_weights = pickle.load(f)
            sentiment_model.set_weights(sentiment_model_weights)
        
        prediction = sentiment_model.predict(report_padded)

        try:
            frauder = FraudulentUser.objects.get(phone_number=spammer_phno)
        except ObjectDoesNotExist:
            frauder = FraudulentUser(
                email=f"{spammer_phno}@gmail.com",
                phone_number=spammer_phno,
                spam_potent=0
            )
            frauder.save()
        
        frauder_reports = Report.objects.filter(spammer=frauder)
        report_count = len(frauder_reports)
        # updated_potent = ((frauder.spam_potent*report_count) + (1-prediction[0])) / (report_count+1)
        updated_potent = ((frauder.spam_potent*report_count) + prediction[0]) / (report_count+1)
        frauder.spam_potent = updated_potent
        frauder.save()

        try:
            reporter = User.objects.get(id=reporter_id)
        except ObjectDoesNotExist:
            return Response({"message": "R!"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            company = Company.objects.get(id=company_id)
        except ObjectDoesNotExist:
            return Response({"message": "C!"}, status=status.HTTP_404_NOT_FOUND)

        try:
            report = Report(
                reporter=reporter,
                spammer=frauder,
                reported_to=company,
                message=report_message
            )
            report.save()
        except Exception as e:
            return Response({"message": getattr(e, "message", repr(e))}, status=status.HTTP_417_EXPECTATION_FAILED)

        return Response({"credibility_score": updated_potent*5, }, status=status.HTTP_200_OK)
