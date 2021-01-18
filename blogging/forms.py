from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, UserProfile, Categories
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm

def get_birth_years():
    year_list = []
    year = 1970
    while year < 2010:
        year_list.append(year)
        year += 1
    return year_list


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('User doest not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect Password')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')
        return super(LoginForm, self).clean(*args, **kwargs)


class PostModelForm(forms.ModelForm):
    category_id = forms.ModelMultipleChoiceField(queryset=Categories.objects.all(),widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Post
        fields = ['title', 'description', 'category_id', 'thumbnail', 'banner']
        labels = {'title':'Post','description':'Content','category_id':'Category','thumbnail':'Thumbnail', 'banner':'Banner'}
        widgets = {
            'title' : forms.TextInput(attrs={'class':'form-control my-2'}),
            'description' : forms.Textarea(attrs={'class':'form-control my-2'}),
            
            'thumbnail' : forms.FileInput(attrs={'class':'d-block'}),
            'banner' : forms.FileInput(attrs={'class':'d-block'})
        }
    

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_img', 'dob', 'qualification']
        labels = {'profile_img':'Profile Image', 'dob':'Date of Birth', 'qualification':'Qualification'}
        widgets = {
            'profile_img':forms.FileInput(attrs={'class':'d-block my-2'}),
            'dob' : forms.SelectDateWidget(years=get_birth_years(),attrs={'class':'form-control my-2'}),
            'qualification' : forms.Select(attrs={'class':'form-control my-2'})
        }

class UserForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control my-2'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control my-2'}))
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        # labels = {}
        widgets = {
            'username' : forms.TextInput(attrs={'class':'form-control my-2'}),
            'first_name' : forms.TextInput(attrs={'class':'form-control my-2'}),
            'last_name' : forms.TextInput(attrs={'class':'form-control my-2'}),
            'email' : forms.EmailInput(attrs={'class':'form-control my-2'}),
            
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        # labels = {}
        widgets = {
            'first_name' : forms.TextInput(attrs={'class':'form-control my-2'}),
            'last_name' : forms.TextInput(attrs={'class':'form-control my-2'}),
            'email' : forms.EmailInput(attrs={'class':'form-control my-2'}),
            
        }