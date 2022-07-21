from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("course/<int:id_cour>/<int:id_from>/<int:id_to>", views.course, name='course'),
]
