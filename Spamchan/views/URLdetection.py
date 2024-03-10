from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
# from .utils import URLdetector  # Import your URLdetector function from your utilities module
from ..scripts.URLMaliciousChecker import download_and_check_files 

class URLDetectionViewSet(viewsets.ViewSet):
    def create(self, request):
        url = request.data.get('url')

        if not url:
            return Response({'error': 'URL not provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Call the download_and_check_files function with the URL
            malicious_percentage = download_and_check_files(url, depth=2)

            # Return the malicious percentage in the response
            return Response({'malicious_percentage': malicious_percentage}, status=status.HTTP_200_OK)
        except Exception as e:
            # Return an error response if an exception occurs
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
