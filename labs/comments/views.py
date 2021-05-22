from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.http import HttpResponse, HttpResponseNotFound
from .forms import SortForm
from .models import *
import json

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
# Create your views here.


class ServMonView(ListView):
    '''Полный список'''
    model = ServMonitor
    queryset = ServMonitor.objects.filter(draft=False)

class ServDetail(DetailView):
    '''Таргетно'''
    model = ServMonitor
    slug_field = "url"


def export(request, pk):
    bd = ServMonitor.objects.get(id=pk)
    data = {'name': bd.name, 'type': bd.type, 'email': bd.email, 'group': bd.group, 'group_type': bd.group_type, 'gps': bd.gps, 'url': bd.url}
    response = HttpResponse(json.dumps(data), content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="members.json"'
    return response


class ServCreateView(CreateView):
    model = ServMonitor
    fields = ('name', 'time', 'type', 'email', 'group', 'group_type', 'gps', 'url')


'''PDF'''
class PdfMakerView(ListView):
    model = PdfMaker
    queryset = PdfMaker.objects.all()
    #template = 'comments\pdfmaker.html'

class PdfMakerDetail(DetailView):
    model = PdfMaker
    slug_field = "url"


class PdfMakerCreateView(CreateView):
    model = PdfMaker
    fields = ('name', 'time', 'type', 'email', 'url')


def pdf_export(request, pk):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    bd = PdfMaker.objects.get(id=pk)
    p.drawString(100, 100, bd.name)
    #p.drawString(100, 150, i.time)
    p.drawString(100, 200, bd.type)
    p.drawString(100, 250, bd.email)
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')


#class SecureView(View):
    '''Отображение только для авторизованных пользователей'''
def index(request):
    context = {
        'servmonitor_list': ServMonitor.objects.filter(draft=False)
        if request.user.is_authenticated else []
    }
    return render(request, 'comments\secure.html', context)

'''class SortView(View):'''
def sort(request):
    form = SortForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data.get("name")
        if data == "all" or data == "All":
            servmonitor = ServMonitor.objects.all()
        else:
            servmonitor = ServMonitor.objects.filter(name=data)
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    return render(request, 'comments\servmonitor_list.html', {'servmonitor_list': servmonitor})
