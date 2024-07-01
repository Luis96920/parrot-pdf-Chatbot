# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from app.forms import uploadForm
from .agent import Agent
from app.models import Profile
import json
from django.http import JsonResponse

def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        login_user = authenticate(request, username=username, password=password)
        if login_user is not None:
            login(request, login_user)
            return redirect('Home')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'Login.html')

def Register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'Login.html')
        try:
            new_user = User.objects.create_user(username=username, email=email, password=password)
            Profile.objects.create(user=new_user)
            messages.success(request, "Registration successful. Please login")
            return render(request, 'Login.html')
        except Exception as e:
            messages.error(request, f"Error with {e}")
            return render(request, 'Login.html')
    else:
        return render(request, 'Login.html')

@login_required
def Home(request):
    form = uploadForm(request.POST, request.FILES)
    chat_history = request.session.get('chat_history', [])
    if request.method == "POST":
        if form.is_valid():
            pdf_document = form.save(commit=False)
            pdf_document.user = request.user
            form.save()
            messages.success(request, "File uploaded successfully")
            return redirect('Home')
        else:
            try:
                data = json.loads(request.body)
                question = data.get('question')
                chat_history = data.get('chat_history',[])
                answer = Agent(question, chat_history)
                chat_history.append({"user": question, "agent": answer})
                request.session['chat_history'] = chat_history
                return JsonResponse({'answer': answer, 'chat_history': chat_history})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
    else:
        context = {"form": uploadForm(),'chat_history': chat_history}
        return render(request, 'Home.html', context)
