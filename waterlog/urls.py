from django.urls import path
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views

#create a list of URLs for this app:
urlpatterns = [
    # path(url, view, name)
    path(r'log', views.ShowTodayWaterView.as_view(), name="show_today_log"),
    path(r'', views.home, name="home1"),
    path(r'log/add', views.AddWaterLogView.as_view(), name="add_waterlog"),
    path(r'log/<int:pk>/delete', views.DeleteWaterLogView.as_view(), name="delete_waterlog"),
    path(r'log/<int:pk>/update', views.UpdateWaterLogView.as_view(), name="update_waterlog"),
    path(r'profile', views.ShowMyProfileView.as_view(), name="my_profile"),
    path(r'profile/create', views.CreateProfileView.as_view(), name = "create_profile"),
    path(r'profile/update', views.UpdateProfileView.as_view(), name ="update_profile"),
    path(r'daily-logs/', views.DailyWaterLogListView.as_view(), name='daily_logs'),
    path(r'logs/<str:date>/', views.ShowDayLogView.as_view(), name='day_log'),
    path(r'friends/', views.ShowFriendsLogView.as_view(), name='friends_log'),
    path(r'friends/add-friends/', views.AddFriendsView.as_view(), name='add_friends'),

    path('login/', auth_views.LoginView.as_view(template_name='waterlog/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='waterlog/log_out.html'), name="logout"),
    path('register/', views.RegistrationView.as_view(), name='register')
]