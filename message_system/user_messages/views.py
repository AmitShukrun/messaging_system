from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Message
from .serializers import MessageSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class MessageListCreateAPIView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class UserMessageListAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(receiver=user)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def unread_messages(request):
    user = request.user
    unread_messages = Message.objects.filter(receiver=user, is_read=False)
    serializer = MessageSerializer(unread_messages, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_user_messages(request, pk, unread=None):
    unread_messages = request.query_params.get('unread')
    if unread_messages:
        # Retrieve all unread messages for the specific user
        unread_messages = Message.objects.filter(is_read=False).values()
        return Response(unread_messages, status=200)

    else:
        messages = Message.objects.filter(sender=pk).values()
        return Response(messages, status=200)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def read_delete_message(request, pk):
    if not request.user.is_authenticated:
        return Response(status=401)

    user = request.user

    try:
        message = Message.objects.get(pk=pk, receiver=user)
    except Message.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = MessageSerializer(message)
        return Response(serializer.data)
    elif request.method == 'PUT':
        message.is_read = True
        message.save()
        return Response(status=204)
    elif request.method == 'DELETE':
        message.delete()
        return Response(status=204)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def write_message(request):
    sender_username = request.data.get('sender')
    receiver_username = request.data.get('receiver')

    try:
        sender = User.objects.get(username=sender_username)
        receiver = User.objects.get(username=receiver_username)
    except User.DoesNotExist:
        return Response({'error': 'Sender or receiver user does not exist.'}, status=400)

    data = {
        'sender': sender.pk,
        'receiver': receiver.pk,
        'subject': request.data.get('subject'),
        'message': request.data.get('message'),
    }

    serializer = MessageSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
