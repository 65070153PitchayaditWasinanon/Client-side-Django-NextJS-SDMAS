from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from SDMAS.models import Room, Student

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    room_id = forms.ModelChoiceField(queryset=Room.objects.all(), label="Room")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name','room_id', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()  # บันทึกข้อมูล User
            student_group = Group.objects.get(name='Student')
            student_group.user_set.add(user)
        return user


class RegisterForm2(UserCreationForm):
    email = forms.EmailField(required=True)
    technician_id = forms.CharField(max_length=20)
    expertise = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email','technician_id', 'expertise', 'first_name', 'last_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()  # บันทึกข้อมูล User
            student_group = Group.objects.get(name='Technician')
            student_group.user_set.add(user)
        return user