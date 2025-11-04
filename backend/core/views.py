from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from GradBond import settings
from authentication.models import alumniProfile, studentProfile
from .models import events, Jobs, University
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from django.conf import settings
import os
from cloudinary.uploader import destroy, upload

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from chat.models import Notification
from django.db.models import Q, F
from django.db.models.functions import Lower


# Create your views here.
def home(request):
    current_date = datetime.now()

    # get all events that date is greater than current date
    # and limit to 3
    event = events.objects.filter(date__gte=current_date).order_by('date')[:3]

    # get all jobs that deadline is greater than current date
    all_jobs = Jobs.objects.filter(deadline__gte=current_date)[:3]

    return render(request, 'core/index.html', {'events': event, 'jobs': all_jobs})


def search_alumni(request):
    if request.method == 'GET':
        university = request.GET.get('university')
        dept = request.GET.get('dept')
        company = request.GET.get('company')
        job_title = request.GET.get('job_title')
        name = request.GET.get('name')
        graduation_year = request.GET.get('graduation_year')
        randomKey = request.GET.get('randomKey') # bubt

        # make sure user at least enter one field
        if not university and not dept and not company and not job_title and not randomKey  and not name and not graduation_year:
            messages.error(request, 'Please enter at least one field to search.')
            return redirect('find-alumni')
        
        # alumni = alumniProfile.objects.select_related('user', 'university').all()
        alumni = alumniProfile.objects.select_related('user', 'university').all().order_by(Lower('full_name'))
        
        if university:
            try:
                uni_id = int(university)
                alumni = alumni.filter(university__id=uni_id)
            except (ValueError, TypeError):
                alumni = alumni.filter(university__name__icontains=university)
        
        if dept:
            alumni = alumni.filter(dept__icontains=dept)
        
        if company:
            alumni = alumni.filter(company__icontains=company)
        
        if job_title:
            alumni = alumni.filter(job_title__icontains=job_title)

        if name:
            alumni = alumni.filter(
                Q(full_name__icontains=name) |
                Q(user__first_name__icontains=name) |
                Q(user__last_name__icontains=name)
            )
        
        # safely handle graduation_year (must be numeric)
        if graduation_year:
            try:
                gy = int(graduation_year)
                alumni = alumni.filter(graduation_year=gy)
            except (ValueError, TypeError):
                pass

        if randomKey:
            # apply OR across multiple fields (search within already filtered queryset)
            random_q = (
                Q(university__name__icontains=randomKey) |
                Q(university__short_name__icontains=randomKey) |
                Q(dept__icontains=randomKey) |
                Q(company__icontains=randomKey) |
                Q(job_title__icontains=randomKey) |
                Q(full_name__icontains=randomKey) |
                Q(user__first_name__icontains=randomKey) |
                Q(user__last_name__icontains=randomKey)
            )
            if randomKey.isdigit():
                try:
                    random_q = random_q | Q(graduation_year=int(randomKey))
                except (ValueError, TypeError):
                    pass
            alumni = alumni.filter(random_q)
        
        return render(request, 'core/alumni_list.html', {'alumni_list': alumni})
    return render(request, 'core/find_alumni.html')

def find_alumni(request):
    university_list = University.objects.all()
    return render(request, 'core/find_alumni.html', {'universities': university_list})

def view_events(request):
    current_date = datetime.now()
    all_events = events.objects.filter(date__gte=current_date)
    return render(request, 'core/event.html', {'events': all_events})

@login_required(login_url='signin')
def add_event(request):
    if request.method == 'POST':
        title = request.POST.get('eventTitle')
        description = request.POST.get('eventDes')
        date = request.POST.get('eventDate')
        time = request.POST.get('eventTime')
        regLink = request.POST.get('eventRegLink')
        location = request.POST.get('eventLocation')
        image = request.FILES.get('eventImage')
        
        event = events(user=request.user, title=title, description=description, date=date, time=time, regLink=regLink ,location=location, image=image)
        event.save()

        try:
            if alumniProfile.objects.filter(user=request.user).exists():
                alumniProfile.objects.filter(user=request.user).update(contributions_count=F('contributions_count') + 1)
        except Exception:
            pass

        messages.success(request, 'Event added successfully. and You won 1 contribution point!')

        students = studentProfile.objects.filter(university=event.user.alumniprofile.university)
        channel_layer = get_channel_layer()

        for student in students:
            notification = Notification.objects.create(
                user=student.user,
                notification_type='event',
                message=f"New event: {event.title}",
                link=f"/event-detail/{event.id}"
            )
            async_to_sync(channel_layer.group_send)(
                f"notifications_{student.user.id}",
                {
                    "type": "send_notification",
                    "notification": {
                        "id": notification.id,
                        "message": notification.message,
                        "type": notification.notification_type,
                        "link": notification.link,
                        "is_read": notification.is_read,
                        "created_at": str(notification.created_at),
                    }
                }
            )
        
        return redirect('profile')
    return render(request, 'core/create_event.html')

@login_required(login_url='signin')
def edit_event(request, id):
    event = events.objects.get(id=id)
    if request.method == 'POST':
        title = request.POST.get('eventTitle')
        description = request.POST.get('eventDes')
        date = request.POST.get('eventDate')
        time = request.POST.get('eventTime')
        regLink = request.POST.get('eventRegLink')
        location = request.POST.get('eventLocation')
        
        if date:
            date = datetime.strptime(date, "%Y-%m-%dT%H:%M")
        
        if time:
            time = datetime.strptime(time, "%H:%M").time()
        
        if 'image' in request.FILES:
            if event.image:
                # Get public_id from the image field
                public_id = event.image.public_id
                if public_id != 'default_cover':
                    destroy(public_id)  # Deletes the old image from Cloudinary
            # Assign new image
            result = upload(
                request.FILES['eventImage'],
                folder='events',
                transformation=[
                    {'quality': 'auto'},
                    {'fetch_format': 'auto'}
                ]
            )
            event.image = result['public_id']  # or result['secure_url']

        
        event.title = title
        event.description = description
        event.date = date
        event.time = time
        event.regLink = regLink
        event.location = location
        event.save()
        messages.success(request, 'Event updated successfully.')
        
        return redirect('profile')
    return render(request, 'core/edit_event.html', {'event': event})

@login_required(login_url='signin')
def delete_event(request, id):
    event = events.objects.get(id=id)

    # Check if the event has an image and delete it from Cloudinary
    if event.image:
        public_id = event.image.public_id
        if public_id != 'default_cover':
            destroy(public_id)

    event.delete()
    messages.success(request, 'Event deleted successfully.')
    return redirect('profile')

def event_detail(request, id):
    event = events.objects.get(id=id)
    return render(request, 'core/event_details.html', {'event': event})

def alumni_list(request):
    return render(request, 'core/alumni_list.html')

@login_required(login_url='signin')
def profile(request):
    user = request.user
    
    email = user.email

    my_event = events.objects.filter(user=user)
    my_jobs = Jobs.objects.filter(user=user)

    isAlumni = False
    if user.is_superuser:
        details = User.objects.get(username=user)
        return render(request, 'core/user_profile.html', {'details': details})

    if alumniProfile.objects.filter(email=email).exists():
        details = alumniProfile.objects.get(user=user)
        isAlumni = True
        return render(request, 'core/user_profile.html', {'details': details, 'isAlumni': isAlumni, 'events': my_event, 'jobs': my_jobs})
    else:
        details = studentProfile.objects.get(user=user)
        return render(request, 'core/user_profile.html', {'details': details})

@login_required(login_url='signin')
def about_user(request, id):
    user = User.objects.get(id=id)
    isAlumni = False
    current_date = datetime.now()
    if alumniProfile.objects.filter(user=user).exists():
        details = alumniProfile.objects.get(user=user)
        user_events = events.objects.filter(user=user).filter(date__gte=current_date)
        user_jobs = Jobs.objects.filter(user=user).filter(deadline__gte=current_date)
        isAlumni = True
        return render(request, 'core/about_user.html', {'details': details, 'isAlumni': isAlumni, 'events': user_events, 'jobs': user_jobs})
    else:
        details = studentProfile.objects.get(user=user)
        return render(request, 'core/about_user.html', {'details': details, 'isAlumni': isAlumni})

@login_required(login_url='signin')
def update_profile(request):
    user = request.user
    email = user.email
    isAlumni = False
    university_list = University.objects.all()

    if alumniProfile.objects.filter(email=email).exists():
        isAlumni = True
        details = alumniProfile.objects.get(user=user)

        if request.method == 'POST':
            details.full_name = request.POST.get('full_name')
            university = request.POST.get('university', '').strip()
            uni_obj = None
            if university:
                try:
                    uni_id = int(university)
                    uni_obj = University.objects.filter(pk=uni_id).first()
                except (ValueError, TypeError):
                    uni_obj, _ = University.objects.get_or_create(name=university)
            else:
                uni_obj = None
            details.university = uni_obj
            details.dept = request.POST.get('dept')
            details.student_id = request.POST.get('student_id')
            details.email = details.email
            details.graduation_year = request.POST.get('graduation_year')
            details.company = request.POST.get('company')
            details.job_title = request.POST.get('job_title')
            details.linkedin = request.POST.get('linkedin')
            user.first_name = details.full_name

            if 'image' in request.FILES:
                # Delete old image from Cloudinary if not default
                if details.image and hasattr(details.image, 'public_id'):
                    public_id = details.image.public_id
                    if public_id != 'default_alumni':
                        destroy(public_id)

                # Upload compressed image to Cloudinary
                result = upload(
                    request.FILES['image'],
                    folder='alumni',
                    transformation=[
                        {'quality': 'auto'},
                        {'fetch_format': 'auto'}
                    ]
                )
                details.image = result['public_id']  # or result['secure_url']

            details.save()
            user.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')

        return render(request, 'core/update_profile.html', {'details': details, 'isAlumni': isAlumni, 'universities': university_list})

    else:
        details = studentProfile.objects.get(user=user)

        if request.method == 'POST':
            details.full_name = request.POST.get('full_name')
            university = request.POST.get('university', '').strip()
            uni_obj = None
            if university:
                try:
                    uni_id = int(university)
                    uni_obj = University.objects.filter(pk=uni_id).first()
                except (ValueError, TypeError):
                    uni_obj, _ = University.objects.get_or_create(name=university)
            else:
                uni_obj = None
            details.university = uni_obj
            details.dept = request.POST.get('dept')
            details.student_id = request.POST.get('student_id')
            details.email = details.email

            if 'image' in request.FILES:
                # Delete old image from Cloudinary if not default
                if details.image and hasattr(details.image, 'public_id'):
                    public_id = details.image.public_id
                    if public_id != 'default_ayh3h7':
                        destroy(public_id)

                # Upload compressed image to Cloudinary
                result = upload(
                    request.FILES['image'],
                    folder='students',
                    transformation=[
                        {'quality': 'auto'},
                        {'fetch_format': 'auto'}
                    ]
                )
                details.image = result['public_id']

            details.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')

        return render(request, 'core/update_profile.html', {'details': details, 'isAlumni': isAlumni, 'universities': university_list})

    return render(request, 'core/update_profile.html', {'universities': university_list})

def view_jobs(request):
    # get all jobs that deadline is greater than current date
    current_date = datetime.now()
    all_jobs = Jobs.objects.filter(deadline__gte=current_date)

    if request.method == 'GET':
        titleComapny = request.GET.get('titleCompany')
        jobType = request.GET.get('jobType')

        # filter jobs based on title or company
        if titleComapny:
            all_jobs = all_jobs.filter(title__icontains=titleComapny) | all_jobs.filter(company__icontains=titleComapny)
        
        # filter jobs based on job type
        if jobType:
            all_jobs = all_jobs.filter(job_type__icontains=jobType)
    return render(request, 'core/jobs.html', {'jobs': all_jobs})

@login_required(login_url='signin')
def create_job(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        title = request.POST.get('jobTitle')
        company = request.POST.get('companyName')
        job_link = request.POST.get('jobLink')
        job_type = request.POST.get('jobType')
        experience = request.POST.get('experience')
        salary = request.POST.get('salary')
        description = request.POST.get('jobDes')
        deadline = request.POST.get('deadline')

        job = Jobs(user=request.user, title=title, company=company, job_link=job_link, job_type=job_type, experience=experience, salary=salary, description=description, deadline=deadline)
        job.save()

        try:
            if alumniProfile.objects.filter(user=request.user).exists():
                alumniProfile.objects.filter(user=request.user).update(contributions_count=F('contributions_count') + 1)
        except Exception:
            pass

        messages.success(request, 'Post your job successfully. and You won 1 contribution point.')

        # Notify all  users about the new job without creator
        channel_layer = get_channel_layer()
        users = User.objects.exclude(id=request.user.id)
        for user in users:
            notification = Notification.objects.create(
                user=user,
                notification_type='job',
                message=f"New job posted: {job.title}",
                link=f"/job-detail/{job.id}"
            )
            async_to_sync(channel_layer.group_send)(
                f"notifications_{user.id}",
                {
                    "type": "send_notification",
                    "notification": {
                        "id": notification.id,
                        "message": notification.message,
                        "type": notification.notification_type,
                        "link": notification.link,
                        "is_read": notification.is_read,
                        "created_at": str(notification.created_at),
                    }
                }
            )
        
        return redirect('profile')
    return render(request, 'core/post_job.html')

@login_required(login_url='signin')
def edit_job(request, id):
    job = Jobs.objects.get(id=id)
    if request.method == 'POST':
        title = request.POST.get('jobTitle')
        company = request.POST.get('companyName')
        job_link = request.POST.get('jobLink')
        job_type = request.POST.get('jobType')
        experience = request.POST.get('experience')
        salary = request.POST.get('salary')
        description = request.POST.get('jobDes')
        deadline = request.POST.get('deadline')

        if deadline:
            deadline = datetime.strptime(deadline, "%Y-%m-%dT%H:%M")

        if title:
            job.title = title

        if company:
            job.company = company
        if job_link:
            job.job_link = job_link
        
        if job_type:
            job.job_type = job_type

        if experience:
            job.experience = experience
        if salary:
            job.salary = salary
        if description:
            job.description = description
        job.save()
        
        messages.success(request, 'Job updated successfully.')
        
        return redirect('profile')
    return render(request, 'core/edit_job.html', {'job': job})

@login_required(login_url='signin')
def delete_job(request, id):
    job = Jobs.objects.get(id=id)
    job.delete()
    messages.success(request, 'Job deleted successfully.')
    return redirect('profile')

def job_detail(request, id):
    job = Jobs.objects.get(id=id)
    return render(request, 'core/job_details.html', {'job': job})


@login_required(login_url='signin')
def contributions_count_api(request):
    try:
        profile = alumniProfile.objects.get(user=request.user)
        return JsonResponse({'contributions_count': profile.contributions_count})
    except alumniProfile.DoesNotExist:
        return JsonResponse({'contributions_count': 0})


# Leaderboard HTML view (authenticated users)
@login_required(login_url='signin')
def leaderboard(request):
    # return top contributors ordered by contributions_count
    top_alumni = alumniProfile.objects.select_related('user', 'university').order_by('-contributions_count')[:100]
    return render(request, 'core/leaderboard.html', {'alumni_list': top_alumni})