# myapp/views.py
from django.shortcuts import render
from django.http import HttpResponse
import os
import openai
from django.http import JsonResponse
from django.contrib.auth.models import User
# At the top of your views.py file, add this line
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Message
from django.shortcuts import render, redirect
from textblob import TextBlob

@login_required(login_url='login')
def home(request):
    context = {
        'username': request.user.username,
        'email': request.user.email
    }
    return render(request, 'chat/notebook.html', context)

openai.api_key  = "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"

def get_completion(prompt, model="gpt-4",temperature=0.9):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message["content"]

def analyze_sentiment(message):
    testimonial = TextBlob(message)
    return testimonial.sentiment

def chat_response(request):
    # This view handles AJAX requests from the front end for ChatGPT responses
    user_input = request.GET.get('input_text')
    if user_input:
        Message.objects.create(user=request.user, text=user_input, is_user_message=True)

        chat_response = get_completion(user_input)
        print("Hello world",chat_response)
        sentiment = analyze_sentiment(user_input)
        print(sentiment)
        Message.objects.create(user=request.user, text=chat_response, is_user_message=False)
        return JsonResponse({'response': chat_response})
    return JsonResponse({'response': ''})


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST.get('email', '')  # Assuming you have an email field in your form
        if not User.objects.filter(username=username).exists():  # Check if user doesn't already exist
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return render(request, 'chat/registration/register/login.html') # Redirect to the home page after registration
        else:
            # Handle the case where a user with the username already exists
            # You might want to return an error message here
            pass
    
    # If it's a GET request or if there was an issue with the form submission
    return render(request, 'chat/registration/register.html', {'error': 'User already exists'})
        
        
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'registration/login.html', {'error': 'Invalid username or password.'})
    else:
        return render(request, 'chat/registration/login.html')
    
        
def logout_view(request):
    logout(request)
    return redirect('login')
