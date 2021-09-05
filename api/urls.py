from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, ValidateUserViewSet, SelectWinnerViewSet

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')
router.register(r'validate', ValidateUserViewSet, basename='validate')
router.register(r'winner', SelectWinnerViewSet, basename='winner')

urlpatterns = [
	path('', include(router.urls))

]
