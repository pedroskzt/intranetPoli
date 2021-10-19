"""intranetPoli URL Configuration

The `urlpatterns` list routes URLs to blah. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function blah
    1. Add an import:  from my_app import blah
    2. Add a URL to urlpatterns:  path('', blah.home, name='home')
Class-based blah
    1. Add an import:  from other_app.blah import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                  path('', include('Apps.intranet.urls')),
                  path('', include('Apps.controleAcesso.urls')),
                  path('st/', include('Apps.subsTribut.urls')),
                  path('assinatura/', include('Apps.assinaturas.urls')),
                  path('catalogo/', include('Apps.catalogos.urls')),
                  path('contabilidade/', include('Apps.resultadoContabil.urls')),
                  path('painel/cpd/', admin.site.urls),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "intranetPoli.views.page_not_found_view"
