from django.urls import path, include
from CDR.views import CDRView, RegisterView, VerifyView, LoginView
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView


router = routers.DefaultRouter()
router.register(r'cdr', CDRView)

urlpatterns = [
    path('', include(router.urls)),
    path('user/register/', RegisterView.as_view()),
    path('user/verify/', VerifyView.as_view()),
    path('user/login/', LoginView.as_view()),
    path('user/token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
]
