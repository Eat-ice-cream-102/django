from django import forms
from captcha.fields import CaptchaField


class UserForm(forms.Form):
    user_email = forms.CharField(label="帳號", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                        'placeholder': '請輸入信箱'}))
    password = forms.CharField(label="密碼", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='驗證碼', error_messages={"invalid": "驗證碼錯誤"})


class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    email = forms.EmailField(label="信箱", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label="用戶名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密碼", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="確認密碼", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    image = forms.ImageField(label="上傳照片")
    phone_number = forms.CharField(label="電話", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    birthday = forms.DateField(label='生日', widget=forms.SelectDateWidget(years=range(2022, 1930, -1)))
    sex = forms.ChoiceField(label='性別', choices=gender)
    captcha = CaptchaField(label='驗證碼', error_messages={"invalid": "驗證碼錯誤"})

