from django import forms
from .models import Student, Teacher, User

FIELDS_CHOICE = (
    ('Math', 'Math'),
    ('Computer Science', 'Computer Science'),
    ('History', 'History'),
)


class StudentForm(forms.ModelForm):
    fields = forms.MultipleChoiceField(choices=FIELDS_CHOICE, widget=forms.CheckboxSelectMultiple)
    password = forms.CharField(min_length=4, widget=forms.PasswordInput(attrs={
        'placeholder': 'Password'
    }))
    password2 = forms.CharField(min_length=4, widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'password2']

    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password and password2 and password != password2:
            raise forms.ValidationError("password and confirm password is not same")
        if len(password) < 4:
            raise forms.ValidationError('Password must be 4 at least')
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.is_student = True
            user.staff = True
            user.set_password(self.cleaned_data['password'])
            user.save()
            Student.objects.create(user=user)
        return user


class TeacherForm(forms.ModelForm):
    fields = forms.MultipleChoiceField(choices=FIELDS_CHOICE, widget=forms.CheckboxSelectMultiple, label='choose your field')
    password = forms.CharField(min_length=4, widget=forms.PasswordInput(attrs={
        'placeholder': 'Password'
    }))
    password2 = forms.CharField(min_length=4, widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password'
    }), label='Confirm Password')

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'password2']

    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password and password2 and password != password2:
            raise forms.ValidationError("password and confirm password is not same")
        if len(password) < 4:
            raise forms.ValidationError('Password must be 4 at least')
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.is_teacher = True
            user.staff = True
            user.set_password(self.cleaned_data['password'])
            user.save()
            Teacher.objects.create(user=user)
        return user
