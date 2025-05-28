from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework.routers import SimpleRouter

from .views import UserViewSet
from .views import ExecutiveMemberViewSet
from .views import PasswordResetRequestView
from .views import PasswordResetConfirmView

router = SimpleRouter()
router.register("users", UserViewSet)
router.register("execmembers", ExecutiveMemberViewSet)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/reset', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('users/reset/confirm', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]

urlpatterns += router.urls