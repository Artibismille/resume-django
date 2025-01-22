

# Create your views here.
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required  # Import login_required here
from django.contrib import messages
from django.contrib.auth.models import User 


def index(request):
    return render(request, 'resume/index.html')



# home
#def home(request):
   # return render(request, 'resume/home.html')




def about_us(request):
    return render(request, 'about.html')


# to call temp1
def temp1(request):
    return render(request, 'resume/temp1.html')

def temp3(request):
    return render(request, 'resume/temp3.html')


# to generate temp1
def generate_pdf(request):
    template_path = 'resume/resume_template.html'
    context = {
        'full_name': request.POST.get('full_name'),
        'address': request.POST.get('address'),
        'phone_number': request.POST.get('phone_number'),
        'email_address': request.POST.get('email_address'),
        'about_yourself': request.POST.get('about_yourself'),
        'experience': request.POST.get('experience'),
        'technical_skills': request.POST.get('technical_skills'),
        'soft_skills': request.POST.get('soft_skills'),
    }
    template = get_template(template_path)
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


#to call temp 2
def temp2(request):
    return render(request, 'resume/temp2.html')

# to generate temp2
def generate_pdf2(request):
    if request.method == 'POST':
        template_path = 'resume/resume_temp2.html'
        context = {
            'full_name': request.POST['full_name'],
            'address': request.POST['address'],
            'phone_number': request.POST['phone_number'],
            'email_address': request.POST['email_address'],
            'skills':request.POST['skills'],
            'about_yourself': request.POST['about_yourself'],
            'experience': request.POST['experience'],
            'technical_skills': request.POST['technical_skills'],
            'soft_skills': request.POST['soft_skills'],
        }
        name=request.POST['full_name']
        # Create a Django template and render it to HTML
        template = get_template(template_path)
        html = template.render(context)

        # Create a PDF object and return it as response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="name.pdf"'

        # Convert HTML to PDF using xhtml2pdf
        pisa_status = pisa.CreatePDF(
            html, dest=response
        )

        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response

    return HttpResponse("Only POST requests are allowed")

def temp2(request):
    return render(request, 'resume/temp2.html')


def generate_pdf3(request):
    if request.method == 'POST':
        # Retrieve data from the form
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        skills = [skill.strip() for skill in request.POST.get('skills', '').split(',')]

        # Retrieve dynamic education fields
        education = []
        education_count = int(request.POST.get('education_count', 0))
        for i in range(1, education_count + 1):
            degree = request.POST.get(f'education_degree_{i}')
            university = request.POST.get(f'education_university_{i}')
            year = request.POST.get(f'education_year_{i}')
            if degree and university and year:
                education.append({'degree': degree, 'university': university, 'year': year})

        # Retrieve dynamic experience fields
        experience = []
        experience_count = int(request.POST.get('experience_count', 0))
        for i in range(1, experience_count + 1):
            job_title = request.POST.get(f'experience_job_title_{i}')
            company = request.POST.get(f'experience_company_{i}')
            years = request.POST.get(f'experience_years_{i}')
            experience.append({'job_title': job_title, 'company': company, 'years': years})

        context = {
            'name': name,
            'email': email,
            'phone': phone,
            'address': address,
            'skills': skills,
            'education': education,
            'experience': experience,
        }

        # Generate PDF
        html = render_to_string('resume/resume_temp1.html', context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="resume.pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return HttpResponse('Error generating PDF', status=500)

        return response

    return render(request, 'resume/temp3.html')



# Signup view
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Sign up successful. Please log in.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('login')

    return render(request, 'signup.html')


# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home after successful login
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            return redirect('login')

    return render(request, 'login.html')


# Home page view (only accessible after login)
@login_required
def home(request):
    return render(request, 'resume/home.html')


def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('index')