from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("group/<str:slug>/", views.group_posts, name="group"),
    path("groups/", views.group_all, name="group_all"),
    path("new/", views.new_post, name="new_post"),
    path("follow/", views.follow_index, name="follow_index"),
]

user_patterns = [
    path("<username>/", views.profile_view, name="profile"),
    path("<username>/<int:post_id>/", views.post_view, name="post"),
    path("<username>/<int:post_id>/edit/", views.post_edit, name="post_edit"),
    path("<username>/<int:post_id>/comment/", views.add_comment, name="add_comment"),
    path("<username>/follow/", views.profile_follow, name="profile_follow"), 
    path("<username>/unfollow/", views.profile_unfollow, name="profile_unfollow"),
]

error_patterns = [
    path("404/", views.page_not_found, name="pnf", kwargs={'exception': Exception("Page not Found!")}),
    path("403/", views.permission_denied, name="pd", kwargs={'exception': Exception("Permission denied!")}),
    path("500/", views.server_error, name="se"),
]
