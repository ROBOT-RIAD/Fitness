# views.py
from django.shortcuts import render
from django.conf import settings
import openai
from django.http import StreamingHttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser
import time
import logging

# Swagger imports
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Configure logging
logger = logging.getLogger(__name__)

openai.api_key = settings.OPENAI_API_KEY

# System prompt
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You are a professional health and fitness advisor. "
        "Provide accurate, safe advice on diet, exercise, and meal planning. "
        "You can suggest weekly plans, food recommendations, and workout tips. "
        "Respond to every user message with a new, relevant response."
    )
}

SESSION_CHAT_HISTORY = {}

class StreamingChatAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    @swagger_auto_schema(
        operation_description="Stream AI chatbot response for health & fitness advice.",
        tags=["Health Chatbot"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["message"],
            properties={
                "message": openapi.Schema(type=openapi.TYPE_STRING, description="User message to the health chatbot"),
                "session_id": openapi.Schema(type=openapi.TYPE_STRING, description="Unique session ID (optional)")
            },
        ),
        responses={200: "Streaming text response"}
    )
    def post(self, request):
        user_input = request.data.get("message")
        session_id = request.data.get("session_id", str(time.time()))  # Unique session_id if not provided

        if not user_input:
            return StreamingHttpResponse("error: no input", status=400)

        # Initialize or get chat history
        if session_id not in SESSION_CHAT_HISTORY:
            SESSION_CHAT_HISTORY[session_id] = [SYSTEM_PROMPT]
        else:
            # Ensure the system prompt is always included
            if SESSION_CHAT_HISTORY[session_id][0] != SYSTEM_PROMPT:
                SESSION_CHAT_HISTORY[session_id].insert(0, SYSTEM_PROMPT)

        chat_history = SESSION_CHAT_HISTORY[session_id]
        chat_history.append({"role": "user", "content": user_input})

        logger.info(f"Received message: {user_input}, session_id: {session_id}")

        # Define a generator to stream the response
        def event_stream():
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4-turbo",
                    messages=chat_history,
                    temperature=0.7,
                    max_tokens=800,
                    stream=True
                )

                full_reply = ""
                for chunk in response:
                    if 'choices' in chunk and len(chunk['choices']) > 0:
                        delta = chunk['choices'][0]['delta']
                        if 'content' in delta:
                            content = delta['content']
                            full_reply += content
                            logger.debug(f"Streaming chunk: {content}")
                            yield content
                            time.sleep(0.05)  # Reduced delay for smoother streaming

                # Save the full response
                chat_history.append({"role": "assistant", "content": full_reply})
                logger.info(f"Completed response: {full_reply}, session_id: {session_id}")

            except Exception as e:
                error_msg = f"\n[ERROR]: {str(e)}"
                logger.error(f"Error in stream: {str(e)}, session_id: {session_id}")
                yield error_msg

        return StreamingHttpResponse(event_stream(), content_type='text/plain')