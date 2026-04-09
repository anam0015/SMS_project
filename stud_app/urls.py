
from django.urls import path, include
from .views import *

urlpatterns = [
    path('login/', login_view, name="login"),
    path('signup/', signup_view, name="signup"),
    path('logout/', logout_view, name="logout"),
    path('home/', home_view, name="student-home"),
    path('get-stud/', get_all_student, name='get-stud'),
    path('insert_one/', insert_student, name='insert'),
    path('update_one/<int:pk>/', update_view, name="update-view"),
    path('delete-one/<int:pk>/',delete_view, name="delete-view"),
    
]