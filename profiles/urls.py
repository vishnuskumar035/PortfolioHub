from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_list, name='user_list'),
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('project/add/', views.add_project, name='add_project'),
    path('project/edit/<int:id>/', views.edit_project, name='edit_project'),
    path('project/delete/<int:id>/', views.delete_project, name='delete_project'),
    path('skills/add/', views.add_skill, name='add_skill'),
    path('skills/edit/<int:skill_id>/', views.edit_skill, name='edit_skill'),
    path('skills/delete/<int:skill_id>/', views.delete_skill, name='delete_skill'),
    path('work_experience/add/', views.add_work_experience, name='add_work_experience'),
    path('work_experience/edit/<int:id>/', views.edit_work_experience, name='edit_work_experience'),
    path('work_experience/delete/<int:id>/', views.delete_work_experience, name='delete_work_experience'),
    path('education/add/', views.add_education, name='add_education'),
    path('education/edit/<int:id>/', views.edit_education, name='edit_education'),
    path('education/delete/<int:id>/', views.delete_education, name='delete_education'),
    path('certification/add/', views.add_certification, name='add_certification'),
    path('certification/edit/<int:id>/', views.edit_certification, name='edit_certification'),
    path('certification/delete/<int:id>/', views.delete_certification, name='delete_certification'),
    path('resume/download/<int:user_id>/', views.download_resume, name='download_resume'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='logout'),
]