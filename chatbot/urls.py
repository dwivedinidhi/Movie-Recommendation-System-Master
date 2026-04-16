"""
URL Configuration for Chatbot
"""
from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.chatbot_page, name='chatbot_page'),
    path('api/chat/', views.chat_message, name='chat_message'),
    path('api/suggestions/', views.get_quick_suggestions, name='get_quick_suggestions'),
    path('api/clear/', views.clear_conversation, name='clear_conversation'),
]