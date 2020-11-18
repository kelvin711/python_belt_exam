from django.urls import path     
from . import views

urlpatterns = [
    path('', views.register_login),
    path('register', views.register),
    path('dashboard', views.dashboard),
    path('login', views.login),
    path('logout', views.logout),
    path('addtrip', views.addtrip),
    path('create_trip', views.create_trip),
    path('joinTrip/<int:travel_id>', views.joinTrip),
    path('cancel/<int:travel_id>', views.cancelTrip),
    path('view/<int:travel_id>', views.tripInfo),
    path('delete/<int:travel_id>', views.delete),
]