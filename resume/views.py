from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

# home
def home(request):
    return render(request, 'resume/home.html')



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

