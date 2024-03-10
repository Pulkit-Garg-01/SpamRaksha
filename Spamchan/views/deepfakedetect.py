# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# # from .deepfake_detection import deepfake_detect_function



# def deepfake_detect_function(video_file):
     
#     result = {'detected': True}
#     return result

# class DeepfakeDetectionView(APIView):
#     def post(self, request):
#         # Assuming the video file is sent in the request data
#         video_file = request.FILES.get('video')
        
#         if video_file is None:
#             return Response({'error': 'No video file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
#         # Call the deepfake detection function
#         result = deepfake_detect_function(video_file)
        
#         # Return the result
#         return Response({'result': result}, status=status.HTTP_200_OK)

import requests
from urllib.parse import urlparse, parse_qs
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

class DeepfakeDetectionView(APIView):
    def post(self, request):
        # Assuming the video URL is sent in the request data
        video_url = request.data.get('video_url')
        
        if not video_url:
            return Response({'error': 'No video URL provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Extract the "v" argument from the video URL
        parsed_url = urlparse(video_url)
        v_argument = parse_qs(parsed_url.query).get('v')
        if not v_argument:
            return Response({'error': 'No "v" argument found in the video URL'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Send a request to the deepfake detection API
        detection_url = f"https://scanner.deepware.ai/public/url/report?video-url={v_argument[0]}"
        print(detection_url)
        response = requests.get(detection_url)
        
        if response.status_code != 200:
            return Response({'error': 'Failed to fetch video report'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Parse the response to determine if the video is deepfaked
        detection_result = response.json()
        
        # Check if any of the detected fields are true
        is_deepfake = any(result['detected'] for result in detection_result['results'].values())
        
        # Return the result
        return Response({'result': {'deepfake': is_deepfake}}, status=status.HTTP_200_OK)
