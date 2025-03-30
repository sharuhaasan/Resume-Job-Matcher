from django.urls import path
from .views import (
    # CandidateProfileCreateView,
    # JobPostingCreateView,
    # JobPostingListView,
    # MatchResultListView,
    ResumeUploadView,
    JobPostingView,
    MatchCandidateToJobView
)

urlpatterns = [
    path("upload-resume/", ResumeUploadView.as_view(), name="upload-resume"),
    path("upload-job/", JobPostingView.as_view(), name="upload-job"),
    path('match/', MatchCandidateToJobView.as_view(), name='match-candidate'),
    # path("upload-resume/", CandidateProfileCreateView.as_view(), name="upload-resume"),
    # path("add-job/", JobPostingCreateView.as_view(), name="add-job"),
    # path("jobs/", JobPostingListView.as_view(), name="job-list"),
    # path("matches/", MatchResultListView.as_view(), name="match-list"),
]
