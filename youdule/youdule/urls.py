from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.contrib.auth import views as auth_views
from vdule.views import top, signup, index, mypage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', top),
    path('signup/', signup),
    path('index/', index, name='index'),
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('auth/', include('social_django.urls', namespace='social')),
    path('mypage/', mypage, name="mypage"),
]
