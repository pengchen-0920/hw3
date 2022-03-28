from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('saml/', include('saml.urls')),
    # path('', views.first_page),
    # path('', views.indexView),
    # path('order/', include('order.urls')),
    path('', include('order.urls')),
    # path('attrs/', views.indexView, name='indexView'),
    # path('order/', views.second_page, name='second_page'),
]
