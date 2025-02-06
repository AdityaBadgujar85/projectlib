from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from students.models import Student 
import logging
from django.db.models import Q
def HomePage(request):
    print(request.user)
    return render(request, 'Homepage.html') 

def AboutPage(request):
    return render(request, 'About.html')

def loginPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Find the user by email
        try:
            user_obj = User.objects.get(email=email)  # Find user with matching email
            username = user_obj.username  # Get the username associated with the email
        except User.DoesNotExist:
            username = None

        # Authenticate using the found username
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('HomePage')
        else:
            # Add an error message for incorrect username or password
            messages.error(request, 'Incorrect username or password!')
            return redirect('Login')  # Redirect to the same login page

    return render(request, 'Login_page.html')

def registerPage(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already in use.')
            return render(request, 'Signup.html', {'name': name, 'email': email})
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'Signup.html', {'name': name, 'email': email})

        username = f"{name}-{email}"
        User.objects.create_user(username=username, email=email, password=password1)
        messages.success(request, 'Registration successful. Please log in.')
        
        return redirect('Login')

    return render(request, 'Signup.html')

def logout_page(request):
    logout(request)
    return redirect('Login')



@login_required
def video_page(request, studid):
    try:
        student_obj = Student.objects.get(id=studid)
        return render(request, 'Video.html', {'student_obj': student_obj})
    except Student.DoesNotExist:
        messages.error(request, 'Student not found.')
        return redirect('Repository')


@login_required
 # Only authenticated users can access this page
def UploadPage(request):
    if request.method == 'POST':
        student_data = {
            'name': request.POST.get('name'),
            'ofclass': request.POST.get('classof'),
            'division': request.POST.get('division'),
            'branch': request.POST.get('branch'),
            'title': request.POST.get('title'),
            'discription': request.POST.get('discription'),
            'video': request.FILES.get('video'),
            'thumbnail': request.FILES.get('thumbnail'),
            'academic_year': request.POST.get('academic_year'),
            'date': request.POST.get('date'),
            'domain': request.POST.get('domain'),
            'Achievements': request.POST.get('achievements'),
            'LevelofProject': request.POST.get('levelofproject'),
            'Challenges': request.POST.get('challenges')
        }

        Student.objects.create(**student_data)
        messages.success(request, 'Project uploaded successfully.')
        return redirect('Repository')
    return render(request, 'UploadPage.html')

@login_required
def RepositoryPage(request):
    # student_list = Student.objects.all()  # Default to all students

    # if request.method == "GET":
    #  st = request.GET.get('search')
    # if st:  # Check if 'search' has a value
    #     student_list = student.objects.filter(
    #         Q(name__icontains=st) | 
    #         Q(title__icontains=st)
    #         # Uncomment additional filters as needed
    #         # Q(academic_year__icontains=st) |
    #         # Q(date__icontains=st) |
    #         # Q(ofclass__icontains=st) |
    #         # Q(division__icontains=st) 
    #     ).distinct()  # Ensures no duplicate results
    # else:
    #     student_list = student.objects.all()  # Default to all students if search is empty


              

    if request.method == "GET":
        
        # Get all selected branches, classes, and domains from the query parameters
        selected_branches = request.GET.getlist('branch')
        selected_classes = request.GET.getlist('ofclass')
        selected_domains = request.GET.getlist('domain')
        selected_search = request.GET.get('search')

        # Filter the student list based on the selected filters
        student_list = Student.objects.all()  # Start with all students

        if selected_branches:
            student_list = student_list.filter(branch__in=selected_branches)

        if selected_classes:
            student_list = student_list.filter(ofclass__in=selected_classes)

        if selected_domains:
            student_list = student_list.filter(domain__in=selected_domains)

        if selected_search:
            student_list = student_list.filter(
                Q(name__icontains=selected_search) |
                Q(title__icontains=selected_search) |
                Q(academic_year__icontains=selected_search) |
                Q(date__icontains=selected_search) |
                Q(ofclass__icontains=selected_search) |
                Q(division__icontains=selected_search) |
                Q(domain__icontains=selected_search)
            ).distinct()  # Ensures no duplicate results

        # Render your template with the filtered student list
    return render(request, 'Repository.html', {'student_list': student_list})



