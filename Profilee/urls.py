from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile_view, name='profile'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path("create-job/", views.create_job, name="create_job"),
    path("view-applicants/<int:job_id>/", views.view_applicants, name="view_applicants"),
    path("job-list", views.job_list, name="job_list"),
    path('job/<int:pk>/', views.JobDetailView.as_view(), name='job_detail'),
]
