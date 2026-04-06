from django.urls import path
from . import views

app_name = 'fraud'

urlpatterns = [
    path('report/<int:post_id>/', views.report_post, name='report_post'),
    path('dashboard/', views.fraud_dashboard, name='dashboard'),
]