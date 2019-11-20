"""market URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.views.generic import TemplateView
from management.controller.TensorflowRequest import TensorflowRequest
from management.controller.Image import Image


urlpatterns = [
    path('admin/', admin.site.urls),
    path('model/', TensorflowRequest.model_request),
    path('images/<str:file_name>', Image.image),
    path('product_image/<str:file_name>', Image.product_image),
    url(r'^', TemplateView.as_view(template_name="index.html")),
]
