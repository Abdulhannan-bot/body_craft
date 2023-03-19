from django.urls import path
from .views import login_page, admin_page, logout_user, admin_zenotiCenter_page, admin_zenotiUsers_page, staff_page, add_admin, admin_employee_profile_page, roster_dashboard_page, roster_missing_report, admin_center_profile_page, admin_position_page, edit_employee_scheduler, edit_employee_roster, edit_position_time, roster_employee_filter, download_csv, report_page, roster_report_page, scheduler_report_page, leave_management_page, edit_employee_leave, email_missing_report, error_log_page

urlpatterns = [
    path('user_login/', login_page, name='user_login'),
    path('user_logout/', logout_user, name='user_logout'),
    path('admin_home_page/', admin_page, name='admin_page'),
    path('roster_dashboard/', roster_dashboard_page,
         name='roster_dashboard'),
    path('roster_employee_filter/', roster_employee_filter,
         name='roster_employee_filter'),
    path('edit_employee_roster/', edit_employee_roster,
         name='edit_employee_roster'),
    path('get_missing_report/', roster_missing_report, name='get_missing_report'),
    path('edit_employee_scheduler/', edit_employee_scheduler,
         name='edit_employee_scheduler'),
    path('body_craft_centers_list/', admin_zenotiCenter_page,
         name='centers_list'),
    path('body_craft_staff_list/', admin_zenotiUsers_page,
         name='staffs_list'),
    path('body_craft_staff_profile/<str:pk>/', admin_employee_profile_page,
         name='body_craft_staff_profile'),
    path('body_craft_center_profile/<str:pk>/', admin_center_profile_page,
         name='body_craft_center_profile'),
    path('position_page/', admin_position_page, name='position_page'),
    path('edit_position_time/', edit_position_time, name='edit_position_time'),
    path('admin_team_page/', add_admin,
         name='admin_team'),
    path('', staff_page, name='staff_home'),
    path('download_csv/', download_csv, name='download_csv'),
    path('reports/', report_page, name='reports'),
    path('roster_reports/', roster_report_page, name='roster_reports'),
    path('scheduler_reports/', scheduler_report_page, name='scheduler_reports'),
    path('staff_leave_management', leave_management_page,
         name='staff_leave_management'),
    path('edit_employee_leave/', edit_employee_leave, name='edit_employee_leave'),
    path('email_missing_report/', email_missing_report,
         name='email_missing_report'),
    path('error_log_page/', error_log_page, name='error_log_page'),


]