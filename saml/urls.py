from django.urls import path, include
from saml import views

urlpatterns = [
    path('sso', views.sso),
    path('acs', views.acs),
    path('slo', views.slo),
    path('sls', views.sls),
    path('metadata', views.metadata),
]
