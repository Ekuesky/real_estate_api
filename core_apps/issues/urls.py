from django.urls import path

from .views import (
    IssueListAPIView,
    IssueCreateAPIView,
    IssueDeleteAPIView,
    IssueUpdateAPIView,
    MyIssuesListAPIView,
    IssueDetailAPIView,
    AssignedIssuesListView,
)


urlpatterns = [
    path("", IssueListAPIView.as_view(), name="issue-list"),
    path("me/", MyIssuesListAPIView.as_view(), name="my-issue-list"),
    path("assigned/", AssignedIssuesListView.as_view(), name="assigned-issues"),
    path(
        "apartments/<uuid:apartment_id>/", IssueCreateAPIView.as_view(), name="create-issue"
    ),
    path("<uuid:id>/", IssueUpdateAPIView.as_view(), name="issue-update"),
    path("<uuid:id>/detail/", IssueDetailAPIView.as_view(), name="issue-detail"),
    path("<uuid:id>/delete/", IssueDeleteAPIView.as_view(), name="delete-issue"),
]