from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from groq import Groq
import json

@login_required
def home_view(request):
    return render(request, 'english_assistant/home.html')

@csrf_exempt
@login_required
def chat_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message')
        
        # Call Groq API
        client = Groq(api_key=settings.GROQ_API_KEY)
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant designed to teach English. Provide clear and concise explanations."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            model="mixtral-8x7b-32768",
            max_tokens=150
        )
        
        # Extract the AI's response
        ai_response = chat_completion.choices[0].message.content
        
        return JsonResponse({'message': ai_response})
    
    # This shouldn't be called directly, but just in case:
    return JsonResponse({'error': 'Invalid request method'}, status=405)