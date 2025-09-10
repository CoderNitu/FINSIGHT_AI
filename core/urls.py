from django.urls import path
from .views import DashboardView, SignUpView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('signup/', SignUpView.as_view(), name='signup'),
]