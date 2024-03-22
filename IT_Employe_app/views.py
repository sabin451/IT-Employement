from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib import messages, auth
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone  
from .models import Department, CustomUser, RegistrationRequest, ProjectModule, ProgressUpdate, Project, ProjectAssignment, ModuleAssignment
from django.contrib.auth import  authenticate, login as a_login
from .models import CustomUser
from django.contrib.auth.decorators import login_required


def login1(request):
    return render(request, 'mainhome.html')


from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

def doLogout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('main_home')  


def main_home(request):
    return render(request, 'mainhome.html')

def admin_home(request):

    unapproved_count = RegistrationRequest.objects.filter(is_approved=False).count()

    return render(request, 'admin_home.html', {
        'unapproved_count': unapproved_count,
    })
    



def developer_home(request):
    developer = CustomUser.objects.all()
    notifications = Notification.objects.filter(recipient=request.user, is_read=False).order_by('-created_at')
    
    # Mark notifications as read
 

    unseen_count = Notification.objects.filter(recipient=request.user, is_read=False).count()
    return render(request, 'developer_home.html', {'developer': developer,'notifications': notifications, 'unseen_count': unseen_count})



def tl_home(request):
    tl = CustomUser.objects.all()  
    notifications = Notification.objects.filter(recipient=request.user)

    # Mark all unread notifications as read
    unread_notifications = notifications.filter(is_read=False)

    return render(request, 'tl_home.html', {'team_lead': tl,'notifications': notifications, 'unread_count': unread_notifications.count()})




from django.shortcuts import render

def user_registration(request):
    departments = Department.objects.all()
    return render(request, 'register_user.html',{'departments': departments})


from django.contrib import messages
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import CustomUser, Department, RegistrationRequest
from django.utils import timezone

def register_user(request):
    if request.method == 'POST':
        # Retrieve form data
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        address = request.POST['address']
        courses_completed = request.POST['courses_completed']
        certification = request.FILES.get('certification')
        department_id = request.POST['department']
        usertype = request.POST.get('usertype')
        username = request.POST['username']  # Retrieve the username from the form

        try:
            department = Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            department = None

        if CustomUser.objects.filter(email=email).exists():
            messages.info(request, 'Email is already registered.')
            return redirect('register_user')

        # Generate a random 8-character password
        random_password = get_random_string(length=8)

        # Create a new CustomUser with the provided username
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=random_password,
            first_name=first_name,
            last_name=last_name,
        )

        user.address = address
        user.courses_completed = courses_completed
        user.certification = certification
        user.department = department
        user.user_type = usertype
        user.save()

        # Create a RegistrationRequest object for approval
        registration_request = RegistrationRequest.objects.create(
            user=user,
            is_approved=False,
            created_at=timezone.now()
        )

        # Send a confirmation email with the random password
        send_mail(
            'Registration Confirmation',
            f'Hello {first_name},\n\n'
            f' Your username is: {username}\n'
            f'Your registration is successful. Your password is: {random_password}',
            'admin@example.com',
            [email],
            fail_silently=False,
        )

        messages.info(request, 'Registration successful. Please check your email for the password.')
        return redirect('login1')  # Redirect to the login page

    # Fetch the list of departments for the registration form
    departments = Department.objects.all()

    return render(request, 'register_user.html', {'departments': departments})






from django.shortcuts import render, redirect
from .models import Department
@login_required(login_url='doLogin')
def add_department(request):
    if request.method == 'POST':
        # Get the department name from the POST request
        department_name = request.POST.get('department_name')

        if department_name:
            # Create a new department and save it to the database
            Department.objects.create(name=department_name)

    # Fetch the list of all departments
    departments = Department.objects.all()

    return render(request, 'add_department.html', {'departments': departments})









from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from .models import CustomUser

def doLogin(request):
    user_name = request.GET.get('username')
    password1 = request.GET.get('password')

    if not (user_name and password1):
        messages.info(request, 'Required fields must be filled in.')
        return redirect('login1')

    user = authenticate(username=user_name, password=password1)

    if not user:
        messages.info(request, 'Login failed. Please check your username and password and try again.')
        return redirect('login1')

    if not user.is_approved and user.user_type != CustomUser.Admin:
        messages.info(request, 'Your account is not yet approved. Please wait for admin approval.')
        return redirect('login1')

    login(request, user)

    if user.user_type == CustomUser.Admin:
        messages.info(request, 'Welcome, ' + str(user_name))
        return redirect('admin_home')
    elif user.user_type == CustomUser.TL:
        messages.info(request, 'Welcome, ' + str(user_name))
        return redirect('tl_home')
    elif user.user_type == CustomUser.Developer:
        messages.info(request, 'Welcome, ' + str(user_name))
        return redirect('developer_home')

    return redirect('login1')

#adminnn.........................................................
@login_required(login_url='doLogin')
def add_project(request):
    if request.method == 'POST':
        client_details = request.POST['client_details']
        project_name = request.POST['project_name']
        description = request.POST['description']
        requirements = request.POST['requirements']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        attachments = request.FILES.get('attachments')
        project_status = request.POST['project_status']

        # You can directly use request.POST['assigned_tl'] without the try-except block
  

        # No need to fetch the department
        # department_id = request.POST['department']
        # department = Department.objects.get(id=department_id)

        project = Project(
            client_details=client_details,
            project_name=project_name,
            description=description,
            requirements=requirements,
            start_date=start_date,
            end_date=end_date,
            attachments=attachments,

            project_status=project_status,
            # Remove the department field
            # department=department
        )
        project.save()

        return redirect('add_project')  # Redirect to a project list view



    return render(request, 'add_project.html')





from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Project, CustomUser, Department, ProjectAssignment, Notification
from django.contrib.auth.decorators import login_required

@login_required(login_url='doLogin')
def assign_project(request):
    if request.method == 'POST':
        project_id = request.POST['project_id']
        team_lead_id = request.POST['team_lead']
        department_id = request.POST['department']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        try:
            project = Project.objects.get(id=project_id)
            team_lead = CustomUser.objects.get(id=team_lead_id, user_type=CustomUser.TL)
            department = Department.objects.get(id=department_id)
        except (Project.DoesNotExist, CustomUser.DoesNotExist, Department.DoesNotExist):
            messages.error(request, 'Invalid project, team lead, or department selected.')
            return redirect('assign_project')

        # Check if the project is already assigned to the Team Lead in the department
        existing_assignment = ProjectAssignment.objects.filter(
            project=project, team_lead=team_lead, department=department
        ).first()
        if existing_assignment:
            messages.error(request, 'This project is already assigned to the selected Team Lead in the department.')
            return redirect('assign_project')

        # Save the project assignment
        project_assignment = ProjectAssignment(
            project=project,
            team_lead=team_lead,
            department=department,
            start_date=start_date,
            end_date=end_date,
        )
        project_assignment.save()

        # Send a notification to the Team Lead
        notification_content = f'You have been assigned to the project "{project.project_name}" in the {department.name} department. Start Date: {start_date}, End Date: {end_date}'
        notification = Notification(
            recipient=team_lead,
            content=notification_content,
            created_at=timezone.now(),
            is_read=False
        )
        notification.save()

        messages.success(request, 'Project assigned successfully.')
        return redirect('assign_project')  # Redirect to a project list view

    # Display the project assignment form
    projects = Project.objects.all()
    team_leads = CustomUser.objects.filter(user_type=CustomUser.TL)
    departments = Department.objects.all()
    return render(request, 'assign_project.html', {'projects': projects, 'team_leads': team_leads, 'departments': departments})


@login_required(login_url='doLogin')
def promote_user(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('user_list')  # Redirect to the user list view

    if user.user_type == '3':
        user.user_type = '2'
        user.save()
        messages.success(request, f'{user.username} promoted to Team Lead successfully.')
    elif user.user_type == '2':
        messages.info(request, f'{user.username} is already a Team Lead.')

    return redirect('user_list')  # Redirect to the user list view

def demote_user(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('user_list')  # Redirect to the user list view

    if user.user_type == '2':
        user.user_type = '3'
        user.save()
        messages.success(request, f'{user.username} demoted to Developer successfully.')
    elif user.user_type == '3':
        messages.info(request, f'{user.username} is already a Developer.')

    return redirect('user_list')  # Redirect to the user list view
@login_required(login_url='doLogin')
def remove_user(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        user.delete()
        messages.success(request, 'User removed successfully.')
    except CustomUser.DoesNotExist:
        messages.error(request, 'User not found.')

    return redirect('user_list')  # Redirect to the user list view
@login_required(login_url='doLogin')
def user_list(request):
    departments = CustomUser.objects.exclude(user_type=1)
    return render(request, 'user_list.html', {'departments': departments})




def project_list(request):
    projects = Project.objects.all()
    return render(request, 'project_list.html', {'projects': projects})


#teamlead..................................................................
# views.py

from django.shortcuts import render, redirect
from .models import Project, ProjectModule, CustomUser, Department, Notification, ProjectAssignment
from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required(login_url='doLogin')
def add_module1(request):
    logged_in_user = request.user

    # Get the assigned projects for the logged-in Team Lead
    assigned_projects = ProjectAssignment.objects.filter(team_lead=logged_in_user).values('project')
    
    # Get the projects assigned to the Team Lead
    projects = Project.objects.filter(id__in=assigned_projects)

    if request.method == 'POST':
        project_id = request.POST.get('project')
        module_name = request.POST.get('module_name')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        assigned_developer_id = request.POST.get('assigned_developer')

        start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()

        try:
            assigned_developer = CustomUser.objects.get(id=assigned_developer_id)
            selected_project = Project.objects.get(id=project_id)

            module = ProjectModule.objects.create(
                project=selected_project,
                module_name=module_name,
                start_date=start_date,
                end_date=end_date,
                assigned_developer=assigned_developer,
                department=assigned_developer.department
            )

            notification_content = f'You have been assigned to the module "{module.module_name}" in the project "{selected_project.project_name}". Start Date: {start_date}, End Date: {end_date}'
            notification = Notification.objects.create(
                recipient=assigned_developer,
                content=notification_content,
                created_at=timezone.now(),
                is_read=False
            )

            return redirect('project_detail', project_id=selected_project.id)

        except CustomUser.DoesNotExist:
            pass

    developers = CustomUser.objects.filter(user_type=CustomUser.Developer)

    return render(request, 'add_module.html', {'projects': projects, 'developers': developers})

from django.shortcuts import render, get_object_or_404
from .models import Project

def project_detail(request, project_id):
 
    project = get_object_or_404(Project, pk=project_id)

    modules = project.modules.all()


    return render(request, 'project_detail.html', {'project': project, 'modules': modules})


from django.shortcuts import render
from .models import ProjectAssignment, ProjectModule

def project_detail_view(request):
    # Assuming the logged-in user is a Team Lead (TL)
    tl_user = request.user

    # Retrieve projects assigned to the TL
    assigned_projects = ProjectAssignment.objects.filter(team_lead=tl_user)
    assigned_project_ids = assigned_projects.values_list('project__id', flat=True)

    # Retrieve modules associated with the assigned projects
    assigned_modules = ProjectModule.objects.filter(project__id__in=assigned_project_ids)

    # You can add more related information retrieval here based on your models

    # Pass the assigned projects and modules as variables to the template
    context = {
        'assigned_projects': assigned_projects,
        'assigned_modules': assigned_modules,
    }

    return render(request, 'project_detail.html', context)



from django.shortcuts import render, get_object_or_404
from .models import CustomUser, ProjectAssignment, Project

def assigned_projects(request, tl_id):
    # Get the team lead (CustomUser with user_type 'TEAMLEAD') using tl_id
    tl = get_object_or_404(CustomUser, id=tl_id, user_type=CustomUser.TL)

    # Get projects assigned to the team lead
    assigned_projects = Project.objects.filter(assignments__team_lead=tl)

    return render(request, 'assigned_projects.html', {'tl': tl, 'assigned_projects': assigned_projects})



from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    user = request.user
    context = {'user': user}
    return render(request, 'profile.html', context)




def view_project_status(request, tl_id):
    tl = CustomUser.objects.get(id=tl_id)
    developers = CustomUser.objects.filter(department=tl.department, user_type='Developer')

    if request.method == 'POST':
        developer_id = request.POST['developer']
        module_id = request.POST['module']

        developer = CustomUser.objects.get(id=developer_id)
        module = ProjectModule.objects.get(id=module_id)
        updates = ProgressUpdate.objects.filter(module=module, department=tl.department, module__assigned_developer=developer)

        return render(request, 'project_status.html', {'tl': tl, 'developers': developers, 'selected_developer': developer, 'module': module, 'updates': updates})

    return render(request, 'view_project_status.html', {'tl': tl, 'developers': developers})



#Developerr...............................................


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ProjectModule

@login_required
def module_assignments(request):
    # Retrieve the currently logged-in user
    developer = request.user

    # Retrieve project modules assigned to the logged-in user
    user_project_modules = ProjectModule.objects.filter(assigned_developer=developer)

    # Render the template with the user's assigned project modules
    return render(request, 'module_assignments.html', {'user_project_modules': user_project_modules ,'developer': developer,})




# project_tracker/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import CustomUser, ProjectModule, ProgressUpdate

def show_add_progress_update(request, module_id):
    # Retrieve the currently logged-in user
    developer = request.user
    
    # Retrieve the project module
    module = get_object_or_404(ProjectModule, id=module_id)

    # Render the 'add_progress_update.html' template with the developer and module
    return render(request, 'add_progress_update.html', {'developer': developer, 'module': module})

# project_tracker/views.py

from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponseBadRequest
from .models import ProgressUpdate  # Import your models

# def add_progress_update(request):
    
#     if request.method == 'POST':
#         developer = request.user
#         module_id = request.POST.get('module_id')
#         modules = ProjectModule.objects.filter(assigned_developer__id=request.user.id)
#         update_text = request.POST.get('update_text')
#         attachment = request.FILES.get('attachments')  # Assuming your file input name is 'attachments'
        
#         # Check if the uploaded file is a PDF
#         if attachment and not attachment.name.endswith('.pdf'):
#             return HttpResponseBadRequest("Only PDF files are allowed.")

#         # Create a new ProgressUpdate instance if the file is a PDF
#         if attachment:
#             progress_update = ProgressUpdate.objects.create(
#                 module_id=module_id,
#                 update_text=update_text,
#                 date=timezone.now().date(),
#                 department=developer.department,
#                 attachments=attachment
#             )
#             return redirect('developer_home')  # Redirect to a success page or any other desired page

#     return render(request, 'add_progress_update.html', {'modules': modules})


# views.py

# views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ProjectModule, ProgressUpdate
from django.utils import timezone

def add_progress_update(request):
    if request.method == 'GET':
        # Render the form with a list of modules
        modules = ProjectModule.objects.all()
        return render(request, 'add_progress_update.html', {'modules': modules})
    elif request.method == 'POST':
        # Handle form submission
        module_id = request.POST.get('module_id')
        update_text = request.POST.get('update_text')
        attachments = request.FILES.get('attachments')

        # Get the selected module
        module = ProjectModule.objects.get(pk=module_id)

        # Create a progress update
        progress_update = ProgressUpdate(
            module=module,
            date=timezone.now().date(),
            update_text=update_text,
            department=module.department  # Assuming department is associated with the module
        )

        # Check if attachments were provided
        if attachments:
            progress_update.attachments = attachments

        progress_update.save()

        messages.success(request, 'Progress update added successfully.')
        return redirect('add_progress_update')


from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def profile1(request):
    user = request.user
    context = {'user': user}
    return render(request, 'profile1.html', context)






# def add_project(request):
#     if request.method == 'POST':
#         client_details = request.POST['client_details']
#         project_name = request.POST['project_name']
#         description = request.POST['description']
#         requirements = request.POST['requirements']
#         start_date = request.POST['start_date']
#         end_date = request.POST['end_date']
#         attachments = request.FILES.get('attachments')
#         assigned_tl_id = request.POST['assigned_tl']
#         project_status = request.POST['project_status']
#         department_id = request.POST['department']

#         try:
#             assigned_tl = CustomUser.objects.get(id=assigned_tl_id)
#         except CustomUser.DoesNotExist:
#             assigned_tl = None

#         try:
#             department = Department.objects.get(id=department_id)
#         except Department.DoesNotExist:
#             department = None

#         project = Project(
#             client_details=client_details,
#             project_name=project_name,
#             description=description,
#             requirements=requirements,
#             start_date=start_date,
#             end_date=end_date,
#             attachments=attachments,
#             assigned_tl=assigned_tl,
#             project_status=project_status,
#             department=department
#         )
#         project.save()

#         return redirect('project_list')  # Redirect to a project list view


#     assigned_tls = CustomUser.objects.filter(user_type='2')  
#     departments = Department.objects.all()
#     return render(request, 'add_project.html', {'assigned_tls': assigned_tls, 'departments': departments})


from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404


from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404



@login_required(login_url='doLogin')
def admin_dashboard(request):

    users_to_approve = CustomUser.objects.exclude(user_type=1)

    return render(request, 'approve_user.html', {'users_to_approve': users_to_approve})



@login_required(login_url='doLogin')
def approve_user(request, user_id):
    user_profile = get_object_or_404(CustomUser, pk=user_id)

    # Approve the user
    user_profile.is_approved = True
    user_profile.save()

    # Delete the associated RegistrationRequest
    registration_request = RegistrationRequest.objects.filter(user=user_profile)
    registration_request.delete()

    # Redirect back to the admin dashboard
    return redirect('admin_dashboard')


@login_required(login_url='doLogin')
def disapprove_user(request, user_id):
    user_profile = get_object_or_404(CustomUser, pk=user_id)

    # Disapprove the user
    user_profile.is_approved = False
    user_profile.save()

    # Redirect back to the admin dashboard
    return redirect('admin_dashboard')


from django.shortcuts import render
from .models import RegistrationRequest

def registration_requests_list(request):
    # Retrieve the list of RegistrationRequest objects
    registration_requests = RegistrationRequest.objects.all()

    # Count the number of unapproved registration requests
    unapproved_count = RegistrationRequest.objects.filter(is_approved=False).count()

    return render(request, 'registration_request_list.html', {
        'registration_requests': registration_requests,
        'unapproved_count': unapproved_count,
    })


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import CustomUser, RegistrationRequest

@login_required(login_url='doLogin')
def registration_requests_list1(request):
    users_to_approve = CustomUser.objects.all()

    # Calculate the number of unapproved registration requests
    unapproved_count = RegistrationRequest.objects.filter(is_approved=False).count()

    return render(request, 'approve_user.html', {
        'users_to_approve': users_to_approve,
        'unapproved_count': unapproved_count,
    })


from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render, redirect
from django.conf import settings


def reset_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        try:
            user = CustomUser.objects.get(username=username, email=email)
            
            # Update user's password
            user.password = make_password(new_password)
            user.save()
            
            update_session_auth_hash(request, user)

            # Send an email to the user with the new password
            subject = 'Password Reset Successful'
            message = f'Your password has been successfully reset. Your new password is: {new_password}'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)

            messages.success(request, 'Password reset successfully. You can now log in with your new password.')
            return redirect('login1')  # Redirect to the login page after a successful password reset
        except CustomUser.DoesNotExist:
            messages.error(request, 'Invalid username or email. Please check your credentials.')
            return redirect('reset_password')
    return render(request, 'reset_password.html')

# views.py

from django.shortcuts import render
from .models import ProgressUpdate
from django.contrib.auth.decorators import login_required

@login_required
def view_uploaded_files(request):
    # Get all progress updates uploaded by the logged-in developer
    uploaded_files = ProgressUpdate.objects.filter(module__assigned_developer=request.user)

    return render(request, 'view_uploaded_files.html', {'uploaded_files': uploaded_files})

# from django.shortcuts import render, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from .models import ProjectModule, ProgressUpdate

# @login_required
# def view_uploaded_pdfs(request):
#     # Get the logged-in user
#     user = request.user

#     # Assuming each user is associated with multiple ProjectModule instances
#     user_modules = ProjectModule.objects.filter(assigned_developer=user)

#     # For simplicity, here we are taking the first module for the logged-in user
#     if user_modules.exists():
#         module = user_modules.first()
#         progress_updates = ProgressUpdate.objects.filter(module=module).exclude(attachments__isnull=True)

#         return render(request, 'view_uploaded_pdfs.html', {'module': module, 'progress_updates': progress_updates})
#     else:
#         # Handle the case where the user has no associated modules
#         return render(request, 'no_modules_assigned.html')


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ProjectModule, ProgressUpdate

@login_required
def view_modules_by_tl(request):
    # Get the logged-in user (assuming the user is a TL)
    tl_user = request.user

    # Assuming the TL is associated with a specific department
    tl_department = tl_user.department

    # Retrieve modules assigned to developers under the TL's department
    modules_by_tl = ProjectModule.objects.filter(department=tl_department, assigned_developer__user_type='3')

    # Retrieve progress updates for the modules
    progress_updates = ProgressUpdate.objects.filter(module__in=modules_by_tl)

    return render(request, 'view_modules_by_tl.html', {'modules_by_tl': modules_by_tl, 'progress_updates': progress_updates})
from django.shortcuts import render, get_object_or_404
from .models import Project, ProgressUpdate

@login_required
def view_uploaded_files_by_project(request):
    # Get all projects to display in the dropdown
    projects = Project.objects.all()

    # Check if the form is submitted
    if request.method == 'POST':
        # Get the selected project ID from the form
        project_id = request.POST.get('project')
        
        # Get the selected project or return 404 if not found
        selected_project = get_object_or_404(Project, id=project_id)
        
        # Get all progress updates related to the selected project
        uploaded_files = ProgressUpdate.objects.filter(module__project=selected_project)
        
        return render(request, 'view_uploaded_files_by_project.html', {'projects': projects, 'uploaded_files': uploaded_files, 'selected_project': selected_project})

    return render(request, 'view_uploaded_files_by_project.html', {'projects': projects})
from django.shortcuts import render
from .models import Notification
from django.contrib.auth.decorators import login_required

@login_required(login_url='doLogin')
def view_notifications(request):
    # Get all notifications received by the logged-in team lead
    notifications = Notification.objects.filter(recipient=request.user)

    # Mark all unread notifications as read
    unread_notifications = notifications.filter(is_read=False)
    unread_notifications.update(is_read=True)

    return render(request, 'view_notifications.html', {'notifications': notifications, 'unread_count': unread_notifications.count()})



from django.shortcuts import render
from .models import Notification
from django.contrib.auth.decorators import login_required

@login_required(login_url='doLogin')
def view_notifications1(request):
    # Get notifications for the logged-in user (developer)
    notifications = Notification.objects.filter(recipient=request.user, is_read=False).order_by('-created_at')
    
    # Mark notifications as read
    notifications.update(is_read=True)

    unseen_count = Notification.objects.filter(recipient=request.user, is_read=False).count()

    return render(request, 'notifications.html', {'notifications': notifications, 'unseen_count': unseen_count})
