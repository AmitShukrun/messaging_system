from .models import Message
from .serializers import MessageSerializer
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_user_messages(request, pk):
    """ This function is responsible for returning user messages """

    try:
        unread_messages = request.query_params.get('unread')
        if unread_messages:
            # Retrieve all unread messages for the specific user
            unread_messages = Message.objects.filter(is_read=False).values()
            return Response({'success': unread_messages}, status=status.HTTP_200_OK)

        else:
            messages = Message.objects.filter(sender=pk).values()
            return Response({'success': messages}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def read_delete_message(request, pk):
    """ In this function we can receive, read and delete a message """

    try:

        if not request.user.is_authenticated:
            return Response("The user is not authenticated", status=status.HTTP_401_UNAUTHORIZED)

        user = request.user

        message = Message.objects.get(pk=pk, receiver=user)

        if request.method == 'GET':
            serializer = MessageSerializer(message)
            return Response({"success": serializer.data}, status=status.HTTP_200_OK)

        elif request.method == 'PUT':
            message.is_read = True
            message.save()

            serializer = MessageSerializer(message)
            return Response({"success": serializer.data}, status=status.HTTP_204_NO_CONTENT)

        elif request.method == 'DELETE':
            message.delete()
            return Response({"success": "The message has been deleted"}, status=status.HTTP_204_NO_CONTENT)

    except Message.DoesNotExist:
        return Response("Message not found", status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def write_message(request):
    """ In this function we write a message """

    sender_username = request.data.get('sender')
    receiver_username = request.data.get('receiver')

    try:
        sender = User.objects.get(username=sender_username)
        receiver = User.objects.get(username=receiver_username)

        data = {
            'sender': sender.pk,
            'receiver': receiver.pk,
            'subject': request.data.get('subject'),
            'message': request.data.get('message'),
        }

        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': serializer.data}, status=status.HTTP_201_CREATED)

        return Response({'error:': serializer.data}, status=status.HTTP_400_BAD_REQUEST)

    except User.DoesNotExist:
        return Response({'error': 'Sender or receiver user does not exist.'}, status=status.HTTP_404_NOT_FOUND)
