from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_home, name='main_home'),
    path('login1/', views.login1, name='login1'),

    # Other URL patterns
    path('add_department/', views.add_department, name='add_department'),

    # Registration URLs
    path('user_registration', views.user_registration, name='user_registration'),
    path('register_user/', views.register_user, name='register_user'),


    # Authentication and User Management URLs
    path('doLogin',views.doLogin,name='doLogin'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('tl_home', views.tl_home, name='tl_home'),
    path('developer_home', views.developer_home, name='developer_home'),
    path('logout/', views.doLogout, name='logout'),

    # Admin URLs
    path('add_project/', views.add_project, name='add_project'),
    path('assign_project/', views.assign_project, name='assign_project'),
    path('promote_user/<int:user_id>/', views.promote_user, name='promote_user'),
    path('demote_user/<int:user_id>/', views.demote_user, name='demote_user'),
    path('remove_user/<int:user_id>/', views.remove_user, name='remove_user'),
    path('user_list/', views.user_list, name='user_list'),
    path('project_list/', views.project_list, name='project_list'),

    # Team Lead URLs
    path('project_detail/',views.project_detail_view, name='project_detail'),
    path('add_module1', views.add_module1, name='add_module1'),
    path('project_detail/<int:project_id>/', views.project_detail, name='project_detail'),
    path('view_project_status/<int:tl_id>/', views.view_project_status, name='view_project_status'),
    path('assigned_projects/<int:tl_id>/', views.assigned_projects, name='assigned_projects'),
    path('profile/', views.profile, name='profile'),

    # Developer URLs
    path('module_assignments/', views.module_assignments, name='module_assignments'),
    path('show_add_progress_update/<int:module_id>/', views.show_add_progress_update, name='show_add_progress_update'),
    path('add_progress_update/', views.add_progress_update, name='add_progress_update'),
    path('profile1/', views.profile1, name='profile1'),



    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('approve_user/<int:user_id>/', views.approve_user, name='approve_user'),
    path('disapprove_user/<int:user_id>/', views.disapprove_user, name='disapprove_user'),
    path('registration_requests/', views.registration_requests_list, name='registration_requests_list'),


    path('reset_password/', views.reset_password, name='reset_password'),
    # path('view_uploaded_pdfs/', views.view_uploaded_pdfs, name='view_uploaded_pdfs'),
    path('view_modules_by_tl/', views.view_modules_by_tl, name='view_modules_by_tl'),
    path('view_uploaded_files/', views.view_uploaded_files, name='view_uploaded_files'),
    path('view_uploaded_files_by_project/', views.view_uploaded_files_by_project, name='view_uploaded_files_by_project'),
    path('view_notifications/', views.view_notifications, name='view_notifications'),
     path('notifications/', views.view_notifications1, name='view_notifications1'),


]
