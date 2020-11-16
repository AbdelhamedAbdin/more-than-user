from django.shortcuts import render
from django.views.generic import CreateView
from .forms import StudentForm, TeacherForm, User
from .models import Student, Teacher
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


def home(request):
    return render(request, 'app1/index.html')


class StudentRegisterView(CreateView):
    form_class = StudentForm
    template_name = 'app1/students.html'
    success_url = reverse_lazy('app1:login')


class TeacherRegisterView(CreateView):
    form_class = TeacherForm
    template_name = 'app1/teachers.html'
    success_url = reverse_lazy('app1:login')


@login_required(login_url=reverse_lazy('app1:login'))
def profile(request, id=None):
    user = User.objects.get(id=id)
    context = {}
    if user.is_teacher:
        context['userprofile'] = Teacher.objects.get(user=user)
    elif user.is_student:
        context['userprofile'] = Student.objects.get(user=user)
    elif user.is_superuser:
        context['userprofile'] = User.objects.get(email=user)
    else:
        context = context
    return render(request, 'app1/profile.html', context)
