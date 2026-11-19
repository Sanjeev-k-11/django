from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .models import Profile


class UserRegisterForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'First Name', 'autocomplete': 'given-name'
    }))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'Last Name', 'autocomplete': 'family-name'
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-input', 'placeholder': 'Email address', 'autocomplete': 'email'
    }))
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'Username', 'autocomplete': 'username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input', 'placeholder': 'Create Password (min 6 characters)', 'autocomplete': 'new-password'
    }))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input', 'placeholder': 'Confirm Password', 'autocomplete': 'new-password'
    }))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose another.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('password_confirm')
        if p1 and p2 and p1 != p2:
            self.add_error('password_confirm', "Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input', 'placeholder': 'Username or Email address', 'autocomplete': 'username', 'id': 'id_username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input', 'placeholder': 'Password', 'autocomplete': 'current-password', 'id': 'id_password'
    }))
    remember_me = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput(attrs={
        'class': 'form-checkbox'
    }))

    def clean(self):
        username = self.cleaned_data.get('username')
        if username and '@' in username:
            user_obj = User.objects.filter(email__iexact=username).first()
            if user_obj:
                self.cleaned_data['username'] = user_obj.username
        return super().clean()


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'institution', 'course_grade', 'daily_study_target_hours', 'bio']
        widgets = {
            'institution': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Stanford University'}),
            'course_grade': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. B.Tech Computer Science'}),
            'daily_study_target_hours': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.5', 'min': '0.5', 'max': '24'}),
            'bio': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Tell us about your academic goals...'}),
            'avatar': forms.FileInput(attrs={'class': 'form-file-input', 'accept': 'image/*'}),
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar and hasattr(avatar, 'size'):
            # Max 5MB
            if avatar.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Avatar image size must be less than 5MB.")
            # Check extension
            ext = avatar.name.split('.')[-1].lower()
            if ext not in ['jpg', 'jpeg', 'png', 'webp', 'gif']:
                raise forms.ValidationError("Unsupported image format. Allowed formats: JPG, PNG, WEBP, GIF.")
        return avatar
