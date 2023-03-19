from django.urls import path
from .views import audit_users, mystery_shopping_overview, mystery_shopping_detail, edit_mystery_shopping_profile, edit_mystery_shopping, edit_mystery_extra_data, edit_audit_user_modal_popup, edit_mystery_audit_status_dropdown, user_search_list
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('audit_users/', audit_users, name='audit_users'),
    path('mystery_shopping/', mystery_shopping_overview,
         name='mystery_shopping'),
    path('mystery_shopping/<str:pk>/', mystery_shopping_detail,
         name='mystery_shopping_detail'),
    path('edit_mystery_shopping_profile/', edit_mystery_shopping_profile,
         name='edit_mystery_shopping_profile'),
    path('edit_mystery_shopping/', edit_mystery_shopping,
         name='edit_mystery_shopping'),
    path('edit_mystery_extra_data/', edit_mystery_extra_data,
         name='edit_mystery_extra_data'),
    path('edit_audit_user_modal_popup/', edit_audit_user_modal_popup,
         name='edit_audit_user_modal_popup'),
    path('edit_mystery_audit_status_dropdown/',
         edit_mystery_audit_status_dropdown, name='edit_mystery_audit_status_dropdown'),
    path('user_search_list/', user_search_list, name='user_search_list'),
    #     path('add_service_agent_to_mystery_shopping/<str:pk>/',
    #          add_service_agent_to_mystery_shopping, name='add_service_agent_to_mystery_shopping'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
