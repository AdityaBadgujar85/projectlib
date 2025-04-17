from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.mail import EmailMessage
from django.conf import settings

from students.models import Student

import logging
import os
from io import BytesIO

# ReportLab imports
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader


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
# def video_page(request, studid):
#     try:
#         student_obj = Student.objects.get(id=studid)
#         return render(request, 'Video.html', {'student_obj': student_obj})
#     except Student.DoesNotExist:
#         messages.error(request, 'Student not found.')
#         return redirect('Repository')
def video_page(request, studid):
    try:
        student_obj = Student.objects.get(id=studid)
        liked = student_obj.likes.filter(id=request.user.id).exists()
        return render(request, 'Video.html', {'student_obj': student_obj ,'liked': liked})
    except Student.DoesNotExist:
        messages.error(request, 'Student not found.')
        return redirect('Repository')


# Register custom fancy script font
font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'Arizonia-Regular.ttf')
pdfmetrics.registerFont(TTFont('Arizonia', font_path))

def generate_certificate(student_obj):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(letter))
    width, height = landscape(letter)

    # Decorative gold border
    margin = 20
    c.setStrokeColorRGB(0.85, 0.65, 0.13)  # gold
    c.setLineWidth(6)
    c.rect(margin, margin, width - 2 * margin, height - 2 * margin)

    # Institute Logo (top-left inside the border)
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'Borcelle.png')
    if os.path.exists(logo_path):
        logo = ImageReader(logo_path)
        # Draw logo before title
        c.drawImage(logo, margin + 30, height - 90, width=120, height=50, mask='auto')

    # Trophy Image (before "Certificate of Excellence" text)
    trophy_image_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'medal.png')
    if os.path.exists(trophy_image_path):
        trophy = ImageReader(trophy_image_path)
        # Adjust size as needed
        c.drawImage(trophy, 60, height - 560, width=150, height=150, mask='auto')
    # Trophy Image (before "Certificate of Excellence" text)
    trophy_image_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'signature.png')
    if os.path.exists(trophy_image_path):
        trophy = ImageReader(trophy_image_path)
        # Adjust size as needed
        c.drawImage(trophy, 580, height - 550, width=130, height=130, mask='auto')
    # Content Y Positions
    y_positions = {
        "title": height - 190,
        "subtitle": height - 240,
        "name": height - 300,
        "project_label": height - 340,
        "project_title": height - 370,
        "domain_date": height - 400,
        "signature_text_y": 70
    }

    # Title with "Certificate of Excellence"
    c.setFont("Helvetica-Bold", 34)
    c.setFillColor(colors.darkblue)
    c.drawCentredString(width / 2, y_positions["title"], "Certificate of Appreciation")

    # Subtitle
    c.setFont("Helvetica", 16)
    c.setFillColor(colors.black)
    c.drawCentredString(width / 2, y_positions["subtitle"], "This certificate is proudly presented to")

    # Student Name
    c.setFont("Arizonia", 44)
    c.setFillColor(colors.darkred)
    c.drawCentredString(width / 2, y_positions["name"], student_obj.name)

    # Project Label
    c.setFont("Helvetica", 14)
    c.setFillColor(colors.black)
    c.drawCentredString(width / 2, y_positions["project_label"], "For their contribution to the LearnVishwa Video Project Library")

    # Project Title
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, y_positions["project_title"], f"\"{student_obj.title}\"")

    # Domain and Date
    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, y_positions["domain_date"], f"Domain: {student_obj.domain}   |   Date: {student_obj.date}")
    
    #Signature
    c.setFont("Helvetica", 12)
    c.drawString(width - 200, y_positions["signature_text_y"], "Authorized Signatory")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

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

        student_obj = Student.objects.create(**student_data)

        # Generate the certificate and get the PDF
        pdf_buffer = generate_certificate(student_obj)

        # Send Email with Certificate
        user_email = request.user.email
        subject = "Thank you for uploading project video on learnvishwa"
        body = f"Dear {request.user.username},\n\nThank you for submitting your project titled \"{student_obj.title}\". Please find your certificate attached.\n\nRegards,\nTeam Learn Vishwa"
        email = EmailMessage(subject, body, to=[user_email])
        email.attach('certificate.pdf', pdf_buffer.getvalue(), 'application/pdf')
        email.send()

        messages.success(request, 'Project uploaded successfully. Certificate sent to your email.')
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

def video_like(request, studid):
    student_obj = get_object_or_404(Student, id=studid)

    if request.user in student_obj.likes.all():
        student_obj.likes.remove(request.user)
        liked = False
    else:
        student_obj.likes.add(request.user)
        liked = True

    return JsonResponse({'liked': liked, 'like_count': student_obj.likes.count()})