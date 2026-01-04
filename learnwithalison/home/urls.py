from django.urls import path
from . import views
from .views import check_superuser


handler400 = "home.views.custom_400"
handler403 = "home.views.custom_403"
handler404 = "home.views.custom_404"
handler500 = "home.views.custom_500"

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('membership/', views.membership, name='membership'),
    path('check_superuser/', check_superuser, name='check_superuser'),
]