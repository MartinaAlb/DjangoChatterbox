from django.shortcuts import render
from django.http import HttpResponse
from base.models import Room

# Create your views here.
def hello(request):
    s = request.GET.get('s','')
    return HttpResponse(f'Ahoj {s}!!!')

def rooms(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, template_name='base/rooms.html', context=context)

