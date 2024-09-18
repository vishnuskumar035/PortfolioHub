import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', default='default.jpg')
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    linkedin_id = models.URLField(blank=True, null=True)
    github_id = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True)
    job_role_1 = models.CharField(max_length=100, blank=True, null=True)
    job_role_2 = models.CharField(max_length=100, blank=True, null=True)
    job_role_3 = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Skill(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=100)
    proficiency = models.PositiveIntegerField()

    def __str__(self):
        return self.skill_name
    
class Project(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
    
class WorkExperience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='work_experience')
    company = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.CharField(max_length=7)  # Format: 'YYYY-MM'
    end_date = models.CharField(max_length=7, blank=True, null=True) 

    def __str__(self):
        return f'{self.position} at {self.company}'
    
    def formatted_start_date(self):
        # Convert 'YYYY-MM' to 'May 2024' format
        return datetime.datetime.strptime(self.start_date, "%Y-%m").strftime("%B %Y")

    def formatted_end_date(self):
        if self.end_date:
            # Convert 'YYYY-MM' to 'May 2024' format
            return datetime.datetime.strptime(self.end_date, "%Y-%m").strftime("%B %Y")
        else:
            # Return 'Present' if end_date is blank
            return "Present"
    
class Education(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='education')
    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    start_date = models.CharField(max_length=7)
    end_date = models.CharField(max_length=7, blank=True, null=True)

    def __str__(self):
        return f'{self.degree} from {self.institution}'
    
    def formatted_start_date(self):
        # Convert 'YYYY-MM' to 'May 2024' format
        return datetime.datetime.strptime(self.start_date, "%Y-%m").strftime("%B %Y")

    def formatted_end_date(self):
        if self.end_date:
            # Convert 'YYYY-MM' to 'May 2024' format
            return datetime.datetime.strptime(self.end_date, "%Y-%m").strftime("%B %Y")
        else:
            # Return 'Present' if end_date is blank
            return "Present"
    
class Certification(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='certification')
    name = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)
    date_obtained = models.CharField(max_length=7)

    def __str__(self):
        return f'{self.name} by {self.organization}'
    
    def formatted_date_obtained(self):
        # Convert 'YYYY-MM' to 'May 2024' format
        return datetime.datetime.strptime(self.date_obtained, "%Y-%m").strftime("%B %Y")
