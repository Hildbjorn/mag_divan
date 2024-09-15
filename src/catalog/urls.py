from django.urls import path
from .views import *

urlpatterns = [
    path('admin/get_all_colors/', get_all_colors, name='get_all_colors'),
    path('admin/get_colors/<int:model_id>/', get_colors, name='get_colors'),
]
