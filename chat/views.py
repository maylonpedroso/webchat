from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from chat.models import ChatMessage, ChatRoom


@login_required(login_url='/user/login')
def room_view(request):
    room_name = request.GET.get('room_name', 'global')
    room, created = ChatRoom.objects.get_or_create(name=room_name)
    messages = ChatMessage.objects.filter(room=room.pk).order_by('-created_at')[:50]
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'latest_messages': reversed(messages),
    })
