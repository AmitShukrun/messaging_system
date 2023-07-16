from django.urls import path
from .views import (
    MessageListCreateAPIView,
    UserMessageListAPIView,
    unread_messages,
    read_delete_message,
    write_message,
    get_user_messages
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


app_name = 'user_messages'

urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('messages/', MessageListCreateAPIView.as_view(), name='message-list-create'),
    path('messages/user/<int:pk>/', read_delete_message, name='read-delete-message'),
    path('users/<int:pk>/messages/', get_user_messages, name='get-all-user_messages'),
    path('messages/unread/', unread_messages, name='unread-messages'),
    path('messages/write/', write_message, name='write-message'),
]
