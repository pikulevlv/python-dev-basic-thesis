from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
from django.core import validators
from .tasks import send_mail_task
from .models import Tool, Order, AdvUser


# класс форм, не связанных с моделью
class ContactForm(forms.Form):
    email = forms.EmailField(widget=forms.
                             TextInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(widget=forms.
                              TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.
                              Textarea(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='Input text',
                           error_messages={'invalid': 'wrong text'})

    def form_valid(self, form):
        subject = form.cleaned_data['subject']
        text = form.cleaned_data['message']
        email = form.cleaned_data['email']
        send_mail_task.delay(subject, text, email)
        return super().form_valid(form)


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your password',
    }))

    class Meta:
        model = AdvUser
        # fields = '__all__'
        fields = ('username', 'first_name', 'last_name', 'email',
                  'password1', 'password2')
        widgets = {'username': forms.TextInput(attrs={
            'placeholder': 'John Gault',
            'class': 'col-md-12form-control'}),
                   'email': forms.EmailInput(attrs={
                       'placeholder': 'your@mail.com',
                       'class': 'col-md-12form-control'}),
                   }


class LoginForm(AuthenticationForm):
    class Meta:
        fields = '__all__'


class ToolForm(forms.ModelForm):
    class Meta:
        model = Tool
        exclude = ('avatar', )


class OrderForm(forms.ModelForm):

    tool = forms.ModelChoiceField(queryset=Tool.objects.all(),
                                  widget=forms.widgets.RadioSelect(),
                                  empty_label=None)
    img = forms.ImageField(validators=[validators.FileExtensionValidator(
        allowed_extensions=('gif', 'png', 'jpg', 'jpeg', 'tif', 'tiff')
    )],
    error_messages={'invalid_extension': 'not supported format'})

    captcha = CaptchaField(label='Input text',
                           error_messages={'invalid': 'wrong text'})

    class Meta:
        model = Order
        exclude = ('user', 'size', 'height', 'width', 'extension',
                   'path', 'string_geodata', 'created', 'discount', 'source_path',
                   'result_folder_path', 'result_path', 'start_datetime',
                   'finish_datetime','task_id',
                   'task_status', 'priority', 'description')
        widgets = {
            'inputed_geodata': forms.widgets.Textarea(attrs={
                'class': 'form-control',
                'cols': 50,
                'rows': 5,
            }),
        }
