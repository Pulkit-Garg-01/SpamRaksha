from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from .deepfake_detection import deepfake_detect_function



def deepfake_detect_function(video_file):
     
    result = {'detected': True}
    return result

class DeepfakeDetectionView(APIView):
    def post(self, request):
        # Assuming the video file is sent in the request data
        video_file = request.FILES.get('video')
        
        if video_file is None:
            return Response({'error': 'No video file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Call the deepfake detection function
        result = deepfake_detect_function(video_file)
        
        # Return the result
        return Response({'result': result}, status=status.HTTP_200_OK)


