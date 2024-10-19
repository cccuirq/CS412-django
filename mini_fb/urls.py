from django.urls import path
from django.conf import settings
from . import views

#create a list of URLs for this app:
urlpatterns = [
    # path(url, view, name)
    path(r'', views.ShowAllProfilesView.as_view(), name = "show_all_profiles"),
    path(r'profile/<int:pk>', views.ShowProfilePageView.as_view(), name = "show_profile"),
    path(r'create_profile', views.CreateProfileView.as_view(), name="create_profile"),
    path(r'profile/<int:pk>/create_status', views.CreateStatusMessageView.as_view(), name="create_status"),
    path(r'profile/<int:pk>/update', views.UpdateProfileView.as_view(), name="update_profile"),
    path(r'status/<int:pk>/delete', views.DeleteStatusMessageView.as_view(), name="delete_status"),
    path(r'status/<int:pk>/update', views.UpdateStatusMessageView.as_view(), name='update_status'),
    path(r'image/<int:pk>/delete', views.DeleteImageView.as_view(), name='delete_image'),
]