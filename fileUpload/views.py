from django.shortcuts import render

from .forms import UploadForm
from django.http import JsonResponse
from .forms import UploadForm
import os
from django.conf import settings
# To extract text from Pdf files
from pdfminer.high_level import extract_text

from .services.openai_service import OpenAiService
from django.conf import settings
from django.http import FileResponse, HttpResponse
from .services.excel_service import ExcelService

from django.core.mail import send_mail, EmailMessage

# Create your views here.
def index(request):
    form = UploadForm()

    return render(request, 'document/index.html', {'form': form})

# Handles the upload of the timesheet file to store it in the media folder
def upload(request):
    if request.FILES:
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():
            timesheet = form.save()
            file_path = timesheet.document.path
            extracted_data = processFile(file_path)

            excel_service = ExcelService()
            out_directory = os.path.join(settings.MEDIA_ROOT, 'processed')

            excel_file_path = excel_service.create_excel(extracted_data, out_directory)

            relative_excel_file_path = os.path.relpath(excel_file_path, settings.MEDIA_ROOT)

            return JsonResponse({'data': extracted_data, 'success': True, 'excel_file_path': relative_excel_file_path})

    return JsonResponse({'data': {}, 'success': False})

# extracts the content of the timesheet file, sends it to the OpenAi API and retrieves the response
def processFile(file_path):
    file_content = extract_text(file_path)
    # initialize the OpenAi Service Class
    openai_service = OpenAiService(api_key=settings.OPENAI_API_KEY)
    # extract the workers name and working hours on every day from the content
    extracted_data = openai_service.extract_data(file_content=file_content)
    return extracted_data






def download_file(request, file_path):
    file_path = os.path.join(settings.MEDIA_ROOT, 'processed', file_path)

    if os.path.join(file_path):
        return FileResponse(open(file_path, 'rb'))
    else:
        return HttpResponse(status=404)
    
def delete_files(path):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            os.unlink(file_path)  # delete file
        except Exception as e:
            print(f'Deleting failed')


def delete_allFiles():
    delete_files(os.path.join(settings.MEDIA_ROOT, 'processed'))
    delete_files(os.path.join(settings.MEDIA_ROOT, 'uploads'))
    



def send_email(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        receiver_email = request.POST.get('receiver_email')
        file_path = request.POST.get('file_path')
        cleaned_path = file_path.replace('media/', '')

        full_file_path = os.path.join(settings.MEDIA_ROOT, cleaned_path.lstrip('/'))
        

        subject = f"Stundenzettel von {name}"
        body = f"Hallo,\n\n{name} hat Ihnen einen Stundenzettel geschickt."

        mail = EmailMessage(subject, body, settings.EMAIL_HOST_USER, [receiver_email])

        mail.attach_file(full_file_path)

        try:
            mail.send()
            return JsonResponse({'success': True, 'message': 'Email sent successfully.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})
    


    





    


