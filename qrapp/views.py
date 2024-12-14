from django.shortcuts import render

# Create your views here.
import qrcode
from django.shortcuts import render
from .forms import URLForm
from io import BytesIO
from django.core.files.base import ContentFile
from django.http import HttpResponse

def generate_qr_code(request):
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(url)
            qr.make(fit=True)
            img = qr.make_image(fill='black', back_color='white')
            img = img.resize((1000, 1000))
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            image_file = ContentFile(buffer.getvalue())
            response = HttpResponse(image_file, content_type="image/png")
            response['Content-Disposition'] = 'attachment; filename="qr_code.png"'
            return response
    else:
        form = URLForm()
    return render(request, 'qrapp/index.html', {'form': form})
