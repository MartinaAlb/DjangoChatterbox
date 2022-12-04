from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, FormView, CreateView

from base.forms import RoomForm
from base.models import Room, Message


# Create your views here.
def hello(request):
    s = request.GET.get('s','')
    return HttpResponse(f'Ahoj {s}!!!')

# def rooms(request):
#     rooms = Room.objects.all()
#     context = {'rooms': rooms}
#     return render(request, template_name='base/rooms.html', context=context)

# class RoomsView(TemplateView):
#     template_name = 'base/rooms.html'
#     extra_context = {'rooms': Room.objects.all()}

class RoomsView(ListView):
    template_name = 'base/rooms.html'
    model = Room
    # musíme v rooms.py zmenit rooms na object_list, ušetříme si jeden select

def room(reguest, id):
    room = Room.objects.get(id=id)
    messages = room.message_set.all()

    # messages = Message.objects.filter(room__id = id)

    context = {'room': room,
        'messages': messages}
    return render(reguest, template_name='base/room.html', context=context)


# class RoomCreateView(FormView):
#     template_name = 'base/room_form.html'
#     form_class = RoomForm
#     success_url = reverse_lazy('rooms')
#
#     def form_valid(self, form):
#         cleaned_data = form.cleaned_data
#         Room.objects.create(
#             name=cleaned_data['name'],
#             description=cleaned_data['description']
#         )
#         return super().form_valid(form)
# změnou formview na createview si ušetříme psaní té funkce, ale musíme do form.py doplnit třídu meta
class RoomCreateView(CreateView):
    template_name = 'base/room_form.html'
    form_class = RoomForm
    success_url = reverse_lazy('rooms')