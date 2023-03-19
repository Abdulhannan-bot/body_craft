from django.urls import path
from .views import clinic_revenue_audit_overview, clinic_revenue_audit_profile_page, edit_clinic_revenue_audit_overview, edit_audit_discount_cases, edit_audit_membership_redemption, edit_audit_clinic_hygiene_check, edit_clinic_audit_deleted_service, edit_clinic_audit_rectification_bill, edit_clinic_audit_other_observation, edit_clinic_audit_not_redeemed, edit_clinic_audit_extra_data
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('clinic_revenue_audit_overview/', clinic_revenue_audit_overview,
         name='clinic_revenue_audit_overview'),
    path('clinic_revenue_audit_profile/<str:pk>/',
         clinic_revenue_audit_profile_page, name='clinic_revenue_audit_profile'),
    path('edit_clinic_revenue_audit_overview/',
         edit_clinic_revenue_audit_overview, name='edit_clinic_revenue_audit_overview'),
    path('edit_clinic_audit_extra_data/', edit_clinic_audit_extra_data,
         name='edit_clinic_audit_extra_data'),
    path('edit_audit_discount_cases/', edit_audit_discount_cases,
         name='edit_audit_discount_cases'),
    path('edit_audit_membership_redemption/', edit_audit_membership_redemption,
         name='edit_audit_membership_redemption'),
    path('edit_audit_clinic_hygiene_check/', edit_audit_clinic_hygiene_check,
         name='edit_audit_clinic_hygiene_check'),
    path('edit_clinic_audit_deleted_service/',
         edit_clinic_audit_deleted_service, name='edit_clinic_audit_deleted_service'),
    path('edit_clinic_audit_rectification_bill/',
         edit_clinic_audit_rectification_bill, name='edit_clinic_audit_rectification_bill'),
    path('edit_clinic_audit_other_observation/',
         edit_clinic_audit_other_observation, name='edit_clinic_audit_other_observation'),
    path('edit_clinic_audit_not_redeemed/', edit_clinic_audit_not_redeemed,
         name='edit_clinic_audit_not_redeemed'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
