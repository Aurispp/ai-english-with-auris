import os
import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from groq import Groq


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def home_view(request):
    return render(request, 'accounts/home.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@csrf_exempt
def chat_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message')
        
        # Call Groq API
        client: Groq = Groq(api_key=settings.GROQ_API_KEY)
        chat_completion = getattr(client.chat.completions, 'create')(
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
            model="mixtral-8x7b-32768",  # or another appropriate model
            max_tokens=150
        )
        
        # Extract the AI's response
        ai_response = chat_completion.choices[0].message.content
        
        return JsonResponse({'message': ai_response})
    
    # This shouldn't be called directly, but just in case:
    return JsonResponse({'error': 'Invalid request method'}, status=405)