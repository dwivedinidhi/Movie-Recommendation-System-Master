"""
Chatbot Views for Movie Recommendation System
"""

import json
import logging
import re
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from .bot_engine import MovieChatbot

logger = logging.getLogger(__name__)

# Global chatbot instance
_chatbot = None


def get_chatbot():
    """Get or create the chatbot instance"""
    global _chatbot
    
    if _chatbot is None:
        # Import the recommender from views
        try:
            from recommender.views import _get_recommender
            recommender = _get_recommender()
            _chatbot = MovieChatbot(recommender=recommender)
        except Exception as e:
            logger.warning(f"Could not initialize chatbot with recommender: {e}")
            _chatbot = MovieChatbot(recommender=None)
    
    return _chatbot


@require_http_methods(["GET"])
def chatbot_page(request):
    """Render the chatbot interface page"""
    return render(request, 'chatbot/chat.html')


@require_http_methods(["POST"])
@csrf_exempt
def chat_message(request):
    """Handle chat messages and return responses"""
    try:
        # Parse the incoming message
        data = json.loads(request.body)
        message = data.get('message', '').strip()
        user_id = data.get('user_id', 'default')
        
        if not message:
            return JsonResponse({
                'success': False,
                'response': "Please type a message.",
                'suggestions': get_chatbot()._get_quick_suggestions()
            })
        
        # Process the message with the chatbot
        chatbot = get_chatbot()
        response_data = chatbot.process_message(message, user_id)
        
        # Format the response
        formatted_response = format_chatbot_response(response_data)
        
        return JsonResponse({
            'success': True,
            'response': formatted_response,
            'raw_response': response_data.get('response', ''),
            'movies': response_data.get('movies', []),
            'suggestions': response_data.get('suggestions', chatbot._get_quick_suggestions()),
            'stage': response_data.get('stage', 'idle')
        })
        
    except Exception as e:
        logger.error(f"Error processing chat message: {e}")
        return JsonResponse({
            'success': False,
            'response': "I'm sorry, I encountered an error. Please try again!",
            'suggestions': get_chatbot()._get_quick_suggestions()
        })


def format_chatbot_response(response_data):
    """Format the chatbot response for display"""
    response = response_data.get('response', '')
    
    # Convert markdown-style bold formatting to HTML
    # Replace **text** with <strong>text</strong>
    response = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', response)
    
    # Convert newlines to <br> tags
    response = response.replace('\n', '<br>')
    
    return response


@require_http_methods(["GET"])
def get_quick_suggestions(request):
    """Get quick suggestion buttons"""
    chatbot = get_chatbot()
    return JsonResponse({
        'suggestions': chatbot._get_quick_suggestions()
    })


@require_http_methods(["POST"])
@csrf_exempt
def clear_conversation(request):
    """Clear the conversation state"""
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id', 'default')
        
        chatbot = get_chatbot()
        chatbot.clear_conversation(user_id)
        
        return JsonResponse({
            'success': True,
            'message': 'Conversation cleared'
        })
    except Exception as e:
        logger.error(f"Error clearing conversation: {e}")
        return JsonResponse({
            'success': False,
            'message': str(e)
        })