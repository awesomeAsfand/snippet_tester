from django.urls import path
from . import views

app_name = 'testt'

urlpatterns = [
    path("", views.create_test, name='create_test'),
    path('detail_test/<int:test_id>', views.detail_test, name='detail_test'),
    path('update-status/<int:test_id>/', views.update_status, name='update_status'),
]
