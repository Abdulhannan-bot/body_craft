from django.urls import path
from .views import revenue_audit_overview, revenue_audit_profile_page, edit_revenue_audit_overview, edit_audit_cashverification, edit_audit_hygiene_check, edit_salon_audit_extra_data, edit_audit_openbill, edit_audit_blockout, edit_audit_pushedappointment, edit_audit_deleted_service, edit_audit_opening_balance, edit_audit_rectification_bill, edit_audit_dcr, edit_audit_otp, edit_audit_campaign_offer, edit_audit_observation, edit_audit_nearby_voucher, edit_audit_pettycash, delete_multiple_salon_hygiene_check, save_salon_hygiene_annexure, add_hygiene_check_from_sheet, save_salon_hygiene_annexure_file, edit_audit_cyber_security

urlpatterns = [
    path('revenue_audit_overview/', revenue_audit_overview,
         name='revenue_audit_overview'),
    path('revenue_audit_profile/<str:pk>/',
         revenue_audit_profile_page, name='revenue_audit_profile'),
    path('edit_revenue_audit_overview/', edit_revenue_audit_overview,
         name='edit_revenue_audit_overview'),
    path('edit_audit_cashverification/', edit_audit_cashverification,
         name='edit_audit_cashverification'),
    path('edit_audit_hygiene_check/', edit_audit_hygiene_check,
         name='edit_audit_hygiene_check'),
    path('edit_salon_audit_extra_data/', edit_salon_audit_extra_data,
         name='edit_salon_audit_extra_data'),
    path('edit_audit_openbill/', edit_audit_openbill, name='edit_audit_openbill'),
    path('edit_audit_blockout/', edit_audit_blockout, name='edit_audit_blockout'),
    path('edit_audit_pushedappointment/', edit_audit_pushedappointment,
         name='edit_audit_pushedappointment'),
    path('edit_audit_deleted_service/', edit_audit_deleted_service,
         name='edit_audit_deleted_service'),
    path('edit_audit_opening_balance/', edit_audit_opening_balance,
         name='edit_audit_opening_balance'),
    path('edit_audit_rectification_bill/', edit_audit_rectification_bill,
         name='edit_audit_rectification_bill'),
    path('edit_audit_dcr/', edit_audit_dcr, name='edit_audit_dcr'),
    path('edit_audit_otp/', edit_audit_otp, name='edit_audit_otp'),
    path('edit_audit_campaign_offer/', edit_audit_campaign_offer,
         name='edit_audit_campaign_offer'),
    path('edit_audit_observation/', edit_audit_observation,
         name='edit_audit_observation'),
    path('edit_audit_nearby_voucher/', edit_audit_nearby_voucher,
         name='edit_audit_nearby_voucher'),
    path('edit_audit_pettycash/', edit_audit_pettycash,
         name='edit_audit_pettycash'),
    path('delete_multiple_salon_hygiene_check/',
         delete_multiple_salon_hygiene_check, name='delete_multiple_salon_hygiene_check'),
    path('save_salon_hygiene_annexure/', save_salon_hygiene_annexure,
         name='save_salon_hygiene_annexure'),
    path('add_hygiene_check_from_sheet/', add_hygiene_check_from_sheet,
         name='add_hygiene_check_from_sheet'),
    path('save_salon_hygiene_annexure_file/', save_salon_hygiene_annexure_file,
         name='save_salon_hygiene_annexure_file'),
    path('edit_audit_cyber_security/', edit_audit_cyber_security,
         name='edit_audit_cyber_security'),
]
