from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework.routers import SimpleRouter

from .views import UserViewSet
from .views import ExecutiveMemberViewSet

router = SimpleRouter()
router.register("users", UserViewSet, basename="users")
router.register("execmembers", ExecutiveMemberViewSet, basename="execmembers")

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls