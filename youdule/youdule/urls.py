from django.contrib import admin
from django.urls import path
from vdule.views import top, signup, index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', top),
    path('signup/', signup),
    path('index/', index, name='index')
]
