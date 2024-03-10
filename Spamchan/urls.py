from django.urls import path,include
from rest_framework import routers
from .views import ReporterViewset
# from .views import
# from .views
from .views.deepfakedetect import DeepfakeDetectionView

router=routers.DefaultRouter()

router.register(r'users',ReporterViewset)
router.register(r'reporters',)

# router.register(r'')
urlpatterns = router.urls

urlpatterns += [
    # path('save_report/', save_report, name='save_report'),
    path('deepfake-detection/', DeepfakeDetectionView.as_view(), name='deepfake_detection'),
    # Other URL patterns...
]