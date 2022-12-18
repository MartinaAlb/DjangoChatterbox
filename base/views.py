from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.db.models import Q
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

@login_required
@permission_required(['base.view_room'])
def search(request):
    q = request.GET.get('q', '')
    rooms = Room.objects.filter(
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    context = {'object_list': rooms}
    return render(request, 'base/rooms.html', context)


# def rooms(request):
#     rooms = Room.objects.all()
#     context = {'rooms': rooms}
#     return render(request, template_name='base/rooms.html', context=context)

# class RoomsView(TemplateView):
#     template_name = 'base/rooms.html'
#     extra_context = {'rooms': Room.objects.all()}

class RoomsView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    template_name = 'base/rooms.html'
    model = Room
    permission_required = 'base.view_room'
    # musíme v rooms.py zmenit rooms na object_list, ušetříme si jeden select


@login_required
@permission_required(['base.view_room', 'base.view_message'])
def room(request, pk):
    room = Room.objects.get(id=pk)

    # POST
    if request.method == 'POST':
        if request.user.has_perm('base.add_message'):
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


class RoomCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = 'base/room_form.html'
    extra_context = {'title' : 'Create new room'}
    form_class = RoomForm
    success_url = reverse_lazy('rooms')
    permission_required = 'base.add_room'

    # zápis do terminálu - slovník, co uživatel zapíše do formuláře - přes logger
    def form_valid(self, form):
        result = super().form_valid(form)
        LOGGER.warning(form.cleaned_data)
        return result


class RoomUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'base/room_form.html'
    extra_context = {'title': 'Update existing room'}
    form_class = RoomForm
    success_url = reverse_lazy('rooms')
    model = Room
    permission_required = 'base.change_room'

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class RoomDeleteView(StaffRequiredMixin, PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    template_name = 'base/room_confirm_delete.html'
    extra_context = {'title': 'careful, you are about to be deleted this room'}
    success_url = reverse_lazy('rooms')
    model = Room
    permission_required = 'base.delete_room'


def handler403(request, exception):
    return render(request, '403.html', status=403)



