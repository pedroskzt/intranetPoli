"""assinaturaEmail URL Configuration

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

from django.urls import path

from Apps.assinaturas.views.assinaturas_email import assinaturas_email
from Apps.assinaturas.views.assinaturas_email import criar_assinatura
from Apps.assinaturas.views.assinaturas_email import visualizar_assinatura
from Apps.assinaturas.views.assinaturas_email import tutoriais

urlpatterns = [
    path('', assinaturas_email, name='index_assinatura'),
    path('criar', criar_assinatura, name='criar_assinatura'),
    path('visualizar', visualizar_assinatura, name='visualizar_assinatura'),
    path('tutoriais/<str:programa_email>', tutoriais, name='tutoriais'),
]
