from django.urls import path

from .views import (
    TagCreateView,
    TagDeleteView,
    TagListView,
    TagUpdateView,
    CurrentSessionAndTermView,
    IndexView,
    SessionCreateView,
    SessionDeleteView,
    SessionListView,
    SessionUpdateView,
    SiteConfigView,
    CourseCreateView,
    CourseDeleteView,
    CourseListView,
    CourseUpdateView,
    TermCreateView,
    TermDeleteView,
    TermListView,
    TermUpdateView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="home"),
    path("site-config", SiteConfigView.as_view(), name="configs"),
    path(
        "current-session/", CurrentSessionAndTermView.as_view(), name="current-session"
    ),
    path("session/list/", SessionListView.as_view(), name="sessions"),
    path("session/create/", SessionCreateView.as_view(), name="session-create"),
    path(
        "session/<int:pk>/update/",
        SessionUpdateView.as_view(),
        name="session-update",
    ),
    path(
        "session/<int:pk>/delete/",
        SessionDeleteView.as_view(),
        name="session-delete",
    ),
    path("term/list/", TermListView.as_view(), name="terms"),
    path("term/create/", TermCreateView.as_view(), name="term-create"),
    path("term/<int:pk>/update/", TermUpdateView.as_view(), name="term-update"),
    path("term/<int:pk>/delete/", TermDeleteView.as_view(), name="term-delete"),
    path("tag/list/", TagListView.as_view(), name="tags"),
    path("tag/create/", TagCreateView.as_view(), name="tag-create"),
    path("tag/<int:pk>/update/", TagUpdateView.as_view(), name="tag-update"),
    path("tag/<int:pk>/delete/", TagDeleteView.as_view(), name="tag-delete"),
    path("course/list/", CourseListView.as_view(), name="courses"),
    path("course/create/", CourseCreateView.as_view(), name="course-create"),
    path(
        "course/<int:pk>/update/",
        CourseUpdateView.as_view(),
        name="course-update",
    ),
    path(
        "course/<int:pk>/delete/",
        CourseDeleteView.as_view(),
        name="course-delete",
    ),
]
