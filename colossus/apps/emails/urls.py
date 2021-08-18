from django.urls import path
from . import views

app_name = 'emails'

urlpatterns = [
    path('get-email/', views.get_email_details, name='get_details'),
]
