from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CreateStory(forms.Form):
    type = forms.ChoiceField(choices=[('Fantasy', 'Fantasy'), ('Western', 'Western'), ('Romance', 'Romance')], label="", widget=forms.Select(attrs={'class' : 'form-control select-multiple'}))
    start = forms.CharField(max_length=250, label="", required=True, widget=forms.TextInput(attrs={'class' : 'form-control text-input-user', 'placeholder' : 'Enter the first sentence of your future storyboard'}))

class CreateStoryHome(forms.Form):
    type = forms.ChoiceField(choices=[('Fantasy', 'Fantasy'), ('Western', 'Western'), ('Romance', 'Romance')], label="", widget=forms.Select(attrs={'class': 'form-control'}))
    start = forms.CharField(max_length=250, label="", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    length = forms.IntegerField(label="", widget=forms.TextInput(attrs={'class': 'form-control'}))

class RegenerateStoryHome(forms.Form):
    regenerate_type = forms.ChoiceField(choices=[('Fantasy', 'Fantasy'), ('Western', 'Western'), ('Romance', 'Romance')], label="", widget=forms.Select(attrs={'class': 'form-control'}))
    regenerate_start = forms.CharField(max_length=250, label="", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    regenerate_length = forms.IntegerField(label="", widget=forms.TextInput(attrs={'class': 'form-control'}))

class ValidationStoryHome(forms.Form):
    type = forms.ChoiceField(choices=[('Fantasy', 'Fantasy'), ('Western', 'Western'), ('Romance', 'Romance')],label="", widget=forms.Select(attrs={'class': 'form-control'}))
    start = forms.CharField(max_length=250, label="", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    length = forms.IntegerField(label="", widget=forms.TextInput(attrs={'class': 'form-control'}))

class SaveStoryboard(forms.Form):
    name = forms.CharField(max_length=100, label="", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    length_storyboard = forms.IntegerField(label="", widget=forms.TextInput(attrs={'class': 'form-control'}))

class ChangeNameStoryboard(forms.Form):
    new_name = forms.CharField(max_length=100, label="", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

class PublishStoryboard(forms.Form):
    publication_message = forms.CharField(max_length=100, label="", required=True, widget=forms.Textarea(attrs={'class': 'form-control publish-text-area'}))