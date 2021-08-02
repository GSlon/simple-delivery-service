from django.urls import path
from mapper import views

urlpatterns = [
    path('', views.default_path),
    path('<int:id>', views.get_map),
]