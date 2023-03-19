from django.urls import path
from .views import corporate_audit_overview, corporate_audit_detail, edit_corporate_audit_overview, edit_corporate_extra_data, edit_corporate_audit_profile
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('corporate_audit_overview/', corporate_audit_overview,
         name='corporate_audit_overview'),
    path('corporate_audit_detail/<str:pk>/', corporate_audit_detail,
         name='corporate_audit_detail'),
    path('edit_corporate_audit_overview/', edit_corporate_audit_overview,
         name='edit_corporate_audit_overview'),
    path('edit_corporate_extra_data/', edit_corporate_extra_data,
         name='edit_corporate_extra_data'),
    path('edit_corporate_audit_profile/', edit_corporate_audit_profile,
         name='edit_corporate_audit_profile'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
