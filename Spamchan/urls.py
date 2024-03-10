from django.urls import path,include
from rest_framework import routers
from .views import ReporterViewset

router=routers.DefaultRouter()
# router.register(r'documents',views.document.DocumentViewset)
router.register(r'users',ReporterViewset)

# router.register(r'')
urlpatterns = router.urls

urlpatterns += [
    # path('save_report/', save_report, name='save_report'),
    # Other URL patterns...
]