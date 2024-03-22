from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth import get_user_model
from django.utils import timezone



class Department(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    Admin = '1'
    TL = '2'
    Developer = '3'
    
    EMAIL_TO_USER_TYPE_MAP = {
        'ADMIN': Admin,
        'TEAMLEAD': TL,
        'DEVELOPER': Developer
    }

    user_type_data = ((Admin, "ADMIN"), (TL, "TEAMLEAD"), (Developer, "DEVELOPER"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)
    
    first_name = models.CharField(max_length=30)  # Add first name
    last_name = models.CharField(max_length=30)  # Add last name

    address = models.TextField(blank=True, null=True)
    courses_completed = models.TextField(blank=True, null=True)
    certification = models.FileField(upload_to='certifications/', blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    is_approved = models.BooleanField(default=False, null=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to',
        related_name='customuser_set'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user',
        related_name='customuser_set'
    )



class PasswordHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    password = models.CharField(max_length=128)  # Store hashed passwords
    created_at = models.DateTimeField(default=timezone.now)

    def __str(self):
        return f"Password history for {self.user.username}"

class Project(models.Model):
    client_details = models.TextField()
    project_name = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    attachments = models.FileField(upload_to='project_attachments/', blank=True, null=True)
    project_status = models.CharField(max_length=20)


class ProjectModule(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='modules')
    module_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    assigned_developer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='modules_assigned_as_developer')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='project_modules')

class ProgressUpdate(models.Model):
    module = models.ForeignKey(ProjectModule, on_delete=models.CASCADE, related_name='progress_updates')
    date = models.DateField()
    update_text = models.TextField()
    attachments = models.FileField(upload_to='progress_attachments/', blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='progress_updates')

class Notification(models.Model):
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications_received', db_index=True, null=True)
    sender = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications_sent')
    content = models.TextField(null=True)
    created_at = models.DateTimeField(default=timezone.now, db_index=True, null=True)
    is_read = models.BooleanField(default=False, null=True)

class ProjectAssignment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='assignments')
    team_lead = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='project_assignments_as_tl')
    start_date = models.DateField()
    end_date = models.DateField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='project_assignments')

class ModuleAssignment(models.Model):
    project_module = models.ForeignKey(ProjectModule, on_delete=models.CASCADE, related_name='assignments')
    developer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='module_assignments_as_developer')
    start_date = models.DateField()
    end_date = models.DateField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='module_assignments')

class RegistrationRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
