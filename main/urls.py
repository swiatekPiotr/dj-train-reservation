from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("course/<int:id_cour>/<int:id_from>/<int:id_to>/<int:id_car>", views.course, name='course'),
    path("create_checkout_session/", views.create_checkout_session, name='create_checkout_session')
]
