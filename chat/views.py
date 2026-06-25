import logging
from django.shortcuts import render
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .ai_service import get_ai_response
from .models import ChatMessage

logger = logging.getLogger(__name__)


@api_view(['POST'])
def chat_view(request):
    logger.debug("Received chat request with data: %s", request.data)
    user_message = request.data.get("message")
    logger.debug("Extracted user message: %s", user_message)

    if not user_message:
        logger.warning("Received chat request without a message.")
        return Response({"error": "Message is required"}, status=400)

    try:
        response = get_ai_response(user_message)
        logger.debug("AI response generated: %s", response)
    except Exception:
        logger.exception("Error while processing chat request.")
        return Response(
            {"error": "Chat service is temporarily unavailable. Please try again later."},
            status=500,
        )
    ChatMessage.objects.create(user_message=user_message, bot_response=response)
    logger.info("Chat request processed successfully.")
    return Response({
        "user": user_message,
        "bot": response
    })