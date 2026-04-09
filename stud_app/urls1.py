from django.urls import path
from .views1 import *

urlpatterns = [
    path('home-view', HomeView.as_view(), name="home"),
    path('get-stud/', StudentListView.as_view(), name="home-get-stud"),

    path('login/', LoginView.as_view(), name="home-login"),
    path('signup/', SignupView.as_view(), name="home-signup"),
    path('logout/', LogoutView.as_view(), name="home-logout"),
    path('insert/', InsertStudentView.as_view(), name="home-insert"),
    path('update/<int:pk>/', UpdateStudentView.as_view(), name="home-update"),
    path('delete/<int:pk>/', DeleteStudentView.as_view(), name="home-delete"),
]