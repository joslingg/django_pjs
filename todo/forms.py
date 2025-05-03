from django import forms
from .models import Task
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("title",) # chỉ cho người dùng nhập title thôi
        
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']
        labels = {
            'username': 'Tên đăng nhập',
            'password1': 'Mật khẩu',
            'password2': 'Xác nhận mật khẩu'
        }
        
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['username'].label = "Tên đăng nhập"
        self.fields['username'].label = "Tên đăng nhập"
        self.fields['password2'].label = "Xác nhận mật khẩu"

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            
        for field in self.fields.values():
            field.widget.attrs.update({'class':'form-control'})