from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import QuizForm_1, QuizForm_2

# Create your views here.
def show_quiz(request):
    if request.method == 'POST':
        form = QuizForm_1(request.POST)
        if form.is_valid():
            form.save()
            currently_experiencing_symptoms = form.cleaned_data.get('currently_experiencing_symptoms')
            if currently_experiencing_symptoms == 'yes':
                return redirect('quiz_2')
            else:
                messages.success(request, f'Form has been Submitted!')
                return redirect('quiz')
    else:
        form = QuizForm_1()
    return render(request, 'quiz/quiz.html', {'form': form})

def show_quiz_2(request):
    if request.method == 'POST':
        form = QuizForm_2(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Form has been Submitted!')
            return redirect('quiz')
    else:
        form = QuizForm_2()
    return render(request, 'quiz/quiz.html', {'form': form})

def home(request):
    return render(request, 'quiz/home.html')