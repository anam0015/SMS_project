
from django.urls import path, include
from .views import *

urlpatterns = [

    #  # Authentication
    # path('login/', login_view, name="login"),
    # path('signup/', signup_view, name="signup"),
    # path('logout/', logout_view, name="logout"),


    #   # Home
    # path('', home_view, name="home"),

    #   # Student CRUD
    # path('students/', get_all_student, name='student-list'),
    # path('students/add/', insert_student, name='student-add'),
    # path('students/update/<int:pk>/', update_view, name="student-update"),
    # path('students/delete/<int:pk>/', delete_view, name="student-delete"),
    
 # Authentication
    path('login/', login_view, name="login"),
    path('signup/', signup_view, name="signup"),
    path('logout/', logout_view, name="logout"),
     # Home
    path('', home_view, name="student-home"),

     # Student CRUD
    path('get-stud/', get_all_student, name='get-stud'),
    path('insert_one/', insert_student, name='insert'),
    path('update_one/<int:pk>/', update_view, name="update-view"),
    path('delete-one/<int:pk>/',delete_view, name="delete-view"),
    #search student
    path('search/', search_student, name='search-student'),
    
]