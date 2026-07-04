"""
URL configuration for FinTrack project.
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('expenses/', include('expenses.urls')),
    path('income/',   include('income.urls')),
    path('budgets/',  include('budgets.urls')),
    
    # Root URL points to the public landing page (Screenshot 2)
    path('', TemplateView.as_view(template_name='landing.html'), name='landing'),
    
    # Protected route home pointing to the simple home details placeholder (Protected by login_required)
    path('home/', login_required(TemplateView.as_view(template_name='home.html')), name='home'),
]

# Support serving media attachments in development environment
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
