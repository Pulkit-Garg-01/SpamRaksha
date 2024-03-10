from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Spamchan.scripts.SpamPotent import getProb
from Spamchan.models import Report, FraudulentUser

class SpamAPIView(APIView):
    """
    API View to calculate probability based on the provided message.
    """

    def post(self, request, *args, **kwargs):
        # Check if 'message' is present in the request data
        if 'message' not in request.data:
            return Response({'error': 'Missing "message" in the request body'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the message from the request data
        message = request.data['message']
        spam_phone = request.data['spamPhone']

        spammer = FraudulentUser.objects.get(phone_number=spam_phone)
        spam_count = Report.objects.filter(spammer=spammer).count()

        # Call the getProb function with the message to calculate probability
        try:
            probability = getProb(message)
            return Response({'probability': probability, 'count': spam_count, 'cred_score': spammer.spam_potent}, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle the exception and return an error response
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
