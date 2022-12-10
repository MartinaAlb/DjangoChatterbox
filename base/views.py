from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, FormView, CreateView, UpdateView, DeleteView

from base.forms import RoomForm, LOGGER
from base.models import Room, Message


# Create your views here.
def hello(request):
    s = request.GET.get('s', '')
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


def room(request, pk):
    room = Room.objects.get(id=pk)

    # POST
    if request.method == 'POST':
        Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        room.save()
        return redirect('room', pk)

    # GET
    messages = room.message_set.all()
    # messages = Message.objects.filter(room__id = id)
    context = {'room': room,
               'messages': messages}
    return render(request, template_name='base/room.html', context=context)


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
    extra_context = {'title' : 'Create new room'}
    form_class = RoomForm
    success_url = reverse_lazy('rooms')

    # zápis do terminálu - slovník, co uživatel zapíše do formuláře - přes logger
    def form_valid(self, form):
        result = super().form_valid(form)
        LOGGER.warning(form.cleaned_data)
        return result

class RoomUpdateView(UpdateView):
    template_name = 'base/room_form.html'
    extra_context = {'title': 'Update existing room'}
    form_class = RoomForm
    success_url = reverse_lazy('rooms')
    model = Room


class RoomDeleteView(DeleteView):
    template_name = 'base/room_confirm_delete.html'
    extra_context = {'title': 'careful, you are about to be deleted this room'}
    success_url = reverse_lazy('rooms')
    model = Room
