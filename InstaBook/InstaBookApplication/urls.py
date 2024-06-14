from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('post', views.post, name='post'),
    path('likepost', views.likepost, name='likepost'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('follow', views.follow, name='follow'),
    path('logout', views.logout, name='logout')
]