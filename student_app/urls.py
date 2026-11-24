from django.urls import path,include
from .views import home,dashboard,registration,create_student,student_list,student_details,update_student,delete_student,signin,signout,StudentViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register("students",StudentViewSet,basename="api-students")

urlpatterns = [
    path("",home,name="home"),
    path("dashboard/",dashboard,name="dashboard"),
    path("registration/",registration,name="registration"),
    path("login/",signin,name="login"),
    path("logout/",signout,name="logout"),
    path("create_student/",create_student,name="create_student"),
    path("students/",student_list,name="students"),
    path("students/<int:pk>/",student_details,name="student_details"),
    path("update_student/<int:pk>/",update_student,name="update_student"),
    path("delete_student/<int:pk>/",delete_student,name="delete_student"),
    path("api/",include(router.urls)),
]