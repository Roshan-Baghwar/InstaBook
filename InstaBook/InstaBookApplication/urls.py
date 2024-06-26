from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('settings', views.settings, name='settings'),
    path('signin', views.signin, name='signin'),
    path('post', views.post, name='post'),
    path('likepost', views.likepost, name='likepost'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('follow', views.follow, name='follow'),
    path('search', views.search, name='search'),
    path('logout', views.logout, name='logout')
]