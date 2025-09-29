from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]
