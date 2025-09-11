from django.urls import path
from . import views

app_name = 'testt'

urlpatterns = [
    path("", views.create_test, name='create_test'),
    path('detail_test/<int:test_id>', views.detail_test, name='detail_test'),
]