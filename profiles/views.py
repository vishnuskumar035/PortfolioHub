from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .forms import ProfileForm, ProjectForm, WorkExperienceForm, EducationForm, CertificationForm, CustomUserCreationForm
from .models import Profile, Project, WorkExperience, Education, Certification, Skill

# Create your views here.

def user_list(req):
    users = Profile.objects.all()
    paginator = Paginator(users, 8)  # 8 users per page
    page_number = req.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(req, 'user/user_list.html', {'page_obj': page_obj})

def user_profile(req, user_id):
    profile = get_object_or_404(Profile, user_id=user_id)
    work_experiences = WorkExperience.objects.filter(profile=profile)
    educations = Education.objects.filter(profile=profile)
    certifications = Certification.objects.filter(profile=profile)
    projects = Project.objects.filter(profile=profile)
    skills = Skill.objects.filter(profile=profile)
    return render(req, 'user/user_profile.html', {
        'profile': profile,
        'work_experiences': work_experiences,
        'educations': educations,
        'certifications': certifications, 
        'projects': projects,
        'skills': skills
    })

@login_required
def edit_profile(req):
    user_profile = get_object_or_404(Profile, user=req.user)
    if req.method == "POST":
        user_profile.first_name = req.POST.get('first_name')
        user_profile.last_name = req.POST.get('last_name')
        user_profile.bio = req.POST.get('bio')
        user_profile.phone = req.POST.get('phone')
        user_profile.email = req.POST.get('email')
        user_profile.linkedin_id = req.POST.get('linkedin_id')
        user_profile.github_id = req.POST.get('github_id')
        if 'image' in req.FILES:
            user_profile.image = req.FILES['image']
        if 'resume' in req.FILES:
            user_profile.resume = req.FILES['resume']
        user_profile.job_role_1 = req.POST.get('job_role_1')
        user_profile.job_role_2 = req.POST.get('job_role_2')
        user_profile.job_role_3 = req.POST.get('job_role_3')
        user_profile.save()
        return redirect('user_profile', user_id=req.user.id)
    return render(req, 'profile/edit_profile.html', {'user_profile': user_profile})

@login_required
def add_skill(req):
    profile = get_object_or_404(Profile, user=req.user)
    if req.method == 'POST':
        skill_name = req.POST.get('skill_name')
        proficiency = req.POST.get('proficiency')
        Skill.objects.create(profile=profile, skill_name=skill_name, proficiency=proficiency)
        return redirect('user_profile', user_id=req.user.id)
    return render(req, 'skill/add_skill.html')

def edit_skill(req, skill_id):
    profile = get_object_or_404(Profile, user=req.user)
    skill = get_object_or_404(Skill, id=skill_id, profile=profile)
    if req.method == 'POST':
        skill.skill_name = req.POST.get('skill_name')
        skill.proficiency = req.POST.get('proficiency')
        skill.save()
        return redirect('user_profile', user_id=req.user.id)
    return render(req, 'skill/edit_skill.html', {'skill': skill})

@login_required
def delete_skill(req, skill_id):
    profile = get_object_or_404(Profile, user=req.user)
    skill = get_object_or_404(Skill, id=skill_id, profile=profile)
    if req.method == 'POST':
        skill.delete()
        return redirect('user_profile', user_id=req.user.id)
    return render(req, 'skill/delete_skill.html', {'skill': skill})

# def project_list(req):
#     projects = Project.objects.all()
#     return render(req, 'project_list.html', {'projects': projects})

@login_required
def add_project(req):
    
    if req.method == 'POST':
        title = req.POST['title']
        description = req.POST['description']
        image = req.FILES['image']
        link = req.POST['link']
        profile = req.user.profile
        Project.objects.create(profile=profile, title=title, description=description, image=image, link=link)
        return redirect('user_profile', user_id=req.user.id)
    return render(req, 'project/add_project.html')

@login_required
def edit_project(req, id):
    project = get_object_or_404(Project, id=id)
    if project.profile.user != req.user:
        return redirect('user_profile', user_id=req.user.id)
    
    if req.method == 'POST':
        project.title = req.POST['title']
        project.description = req.POST['description']
        project.image = req.FILES['image'] if 'image' in req.FILES else project.image
        project.link = req.POST['link']
        project.save()
        return redirect('user_profile', user_id=req.user.id)
    return render(req, 'project/edit_project.html', {'project': project})

@login_required
def delete_project(req, id):
    project = get_object_or_404(Project, id=id, profile=req.user.profile)
    if req.method == 'POST':
        project.delete()
        return redirect('user_profile', user_id=req.user.id)
    return render(req, 'project/delete_project.html', {'project': project}) 

# @login_required
# def work_experience_list(request):
#     experiences = WorkExperience.objects.filter(profile=request.user.profile)
#     return render(request, 'work_experience_list.html', {'experiences': experiences})

@login_required
def add_work_experience(req):
    if req.method == 'POST':
        company = req.POST.get('company')
        position = req.POST.get('position')
        start_date = req.POST.get('start_date')
        end_date = req.POST.get('end_date')
        description = req.POST.get('description')
        profile = req.user.profile
        WorkExperience.objects.create(
            profile=profile,
            company=company,
            position=position,
            start_date=start_date,
            end_date=end_date,
            description=description
        )
        return redirect('user_profile', user_id=req.user.id)
    return render(req, 'experience/add_work_experience.html')

@login_required
def edit_work_experience(req, id):
    work_experience = get_object_or_404(WorkExperience, id=id)
    if work_experience.profile.user != req.user:
        return redirect('user_profile', user_id=req.user.id)
    
    if req.method == "POST":
        work_experience.position = req.POST.get('position')
        work_experience.company = req.POST.get('company')
        work_experience.start_date = req.POST.get('start_date')
        work_experience.end_date = req.POST.get('end_date')
        work_experience.description = req.POST.get('description')
        work_experience.save()
        return redirect('user_profile', user_id=req.user.id)
    
    return render(req, 'experience/edit_experience.html', {'work_experience': work_experience})

@login_required
def delete_work_experience(req, id):
    experience = get_object_or_404(WorkExperience, id=id, profile=req.user.profile)
    if req.method == 'POST':
        experience.delete()
        return redirect('user_profile', user_id=req.user.id)
    return render(req, 'experience/delete_experience.html', {'experience': experience})


# @login_required
# def education_list(request):
#     education_list = Education.objects.filter(profile=request.user.profile)
#     return render(request, 'education_list.html', {'education_list': education_list})

@login_required
def add_education(req):
    if req.method == 'POST':
        institution = req.POST.get('institution')
        degree = req.POST.get('degree')   
        start_date = req.POST.get('start_date')
        end_date = req.POST.get('end_date')
        profile = req.user.profile
        Education.objects.create(
            profile=profile,
            institution=institution,
            degree=degree,
            start_date=start_date,
            end_date=end_date
        )
        return redirect('user_profile', user_id=req.user.id)
    return render(req, 'education/add_education.html')

@login_required
def edit_education(req, id):
    education = get_object_or_404(Education, id=id)
    if education.profile.user != req.user:
        return redirect('user_profile', user_id=req.user.id)
    
    if req.method == 'POST':
        education.degree = req.POST.get('degree')
        education.institution = req.POST.get('institution')
        education.start_date = req.POST.get('start_date')
        education.end_date = req.POST.get('end_date')
        education.save()
        return redirect('user_profile', user_id=req.user.id)
    return render(req, 'education/edit_education.html', {'education': education})

@login_required
def delete_education(req, id):
    education = get_object_or_404(Education, id=id, profile=req.user.profile)
    if req.method == 'POST':
        education.delete()
        return redirect('user_profile', user_id=req.user.id)
    return render(req, 'education/delete_education.html', {'education': education})

# @login_required
# def certification_list(request):
#     certifications = Certification.objects.filter(profile=request.user.profile)
#     return render(request, 'certification_list.html', {'certifications': certifications})

@login_required
def add_certification(req):
    if req.method == 'POST':
        name = req.POST.get('name')
        organization = req.POST.get('organization')
        date_obtained = req.POST.get('date_obtained')
        profile = req.user.profile
        Certification.objects.create(
            profile=profile,
            name=name,
            organization=organization,
            date_obtained=date_obtained
        )
        return redirect('user_profile', user_id=req.user.id)
    return render(req, 'certification/add_certification.html')

@login_required
def edit_certification(req, id):

    certification = get_object_or_404(Certification, id=id)
    if certification.profile.user != req.user:
        return redirect('user_profile', user_id=req.user.id)
    
    if req.method == 'POST':
        certification.name = req.POST.get('name')
        certification.organization = req.POST.get('organization')
        certification.date_obtained = req.POST.get('date_obtained')
        
        certification.save()
        return redirect('user_profile', user_id=req.user.id)
    return render(req, 'certification/edit_certification.html', {'certification': certification})

@login_required
def delete_certification(req, id):
    certification = get_object_or_404(Certification, id=id, profile=req.user.profile)
    if req.method == 'POST':
        certification.delete()
        return redirect('user_profile', user_id=req.user.id)
    return render(req, 'certification/delete_certification.html', {'certification': certification})

def download_resume(req, user_id):
    profile = get_object_or_404(Profile, user_id=user_id)
    if profile.resume:
        response = HttpResponse(profile.resume, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename={profile.user.username}_resume.pdf'
        return response
    else:
        return HttpResponse("Resume not found.")

def register(req):
    if req.method == 'POST':
        username = req.POST['username']
        password = req.POST['password']
        email = req.POST['email']
        first_name = req.POST['first_name']
        last_name = req.POST['last_name']
        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        Profile.objects.create(user=user, email=email, phone=req.POST['phone'])
        login(req, user)
        return redirect('user_list')
    return render(req, 'auth/register.html')

def user_login(req):
    if req.method == 'POST':
        username = req.POST['username']
        password = req.POST['password']
        user = authenticate(req, username=username, password=password)
        if user is not None:
            login(req, user)
            return redirect('user_list')
        else:
            return render(req, 'login.html', {'error': 'Invalid credentials'})
    return render(req, 'auth/login.html')

@login_required
def user_logout(req):
    logout(req)
    return redirect('user_login')