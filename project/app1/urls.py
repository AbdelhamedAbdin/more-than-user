from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect

app_name = 'app1'


class Login(LoginView):
    template_name = 'app1/login.html'

    def get_success_url(self):
        return reverse_lazy('app1:user_profile', args=[self.request.user.id])

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, 'username or password are invalid. please try again.', extra_tags='validate_form')
        return redirect('app1:login')


urlpatterns = [
    path('', views.home, name='index'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='app1/logout.html', next_page=reverse_lazy('app1:login')), name='logout'),
    path('register-teachers/', views.TeacherRegisterView.as_view(), name='teacher-register'),
    path('register-students/', views.StudentRegisterView.as_view(), name='student-register'),
    path('profile/<int:id>/', views.profile, name='user_profile'),
]
