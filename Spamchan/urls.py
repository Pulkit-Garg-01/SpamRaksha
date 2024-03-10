from django.urls import path,include
from rest_framework import routers
from .views import ReporterViewset
# from .views import
# from .views
from .views.deepfakedetect import DeepfakeDetectionView
from .views.URLdetection import URLDetectionViewSet

router=routers.DefaultRouter()

router.register(r'users',ReporterViewset)
router.register(r'reporters',ReporterViewset)

# router.register(r'')
# urlpatterns = router.urls

urlpatterns = [
    # path('save_report/', save_report, name='save_report'),
    path('', include(router.urls)),
    path('deepfake-detection/', DeepfakeDetectionView.as_view(), name='deepfake_detection'),
    path('URLdetection/',URLDetectionViewSet.as_view({'post': 'create'}),name='URL_detetion'),
    # Other URL patterns...
]