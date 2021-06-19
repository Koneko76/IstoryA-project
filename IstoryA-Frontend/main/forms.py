from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class createStory(forms.Form):
    typeStory = forms.ChoiceField(choices=[('Fantasy', 'Fantasy'), ('Horror', 'Horror'), ('Romance', 'Romance')], label="", widget=forms.Select(attrs={'class' : 'form-control select-multiple'}))
    startStory = forms.CharField(max_length=250, label="", required=True, widget=forms.TextInput(attrs={'class' : 'form-control text-input-user', 'placeholder' : 'Enter the first sentence of your future storyboard'}))

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class createStoryHome(forms.Form):
	typeStory = forms.ChoiceField(choices=[('Fantasy', 'Fantasy'), ('Horror', 'Horror'), ('Romance', 'Romance')], label="", widget=forms.Select(attrs={'class': 'form-control'}))
	startStory = forms.CharField(max_length=250, label="", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
	lengthStory = forms.IntegerField(label="", widget=forms.TextInput(attrs={'class': 'form-control'}))

class regenerateStoryHome(forms.Form):
	regenerateTypeStory = forms.ChoiceField(choices=[('Fantasy', 'Fantasy'), ('Horror', 'Horror'), ('Romance', 'Romance')], label="", widget=forms.Select(attrs={'class': 'form-control'}))
	regenerateStartStory = forms.CharField(max_length=250, label="", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
	regenerateLengthStory = forms.IntegerField(label="", widget=forms.TextInput(attrs={'class': 'form-control'}))

class validationStoryHome(forms.Form):
		typeStoryValidation = forms.ChoiceField(choices=[('Fantasy', 'Fantasy'), ('Horror', 'Horror'), ('Romance', 'Romance')],label="", widget=forms.Select(attrs={'class': 'form-control'}))
		startStoryValidation = forms.CharField(max_length=250, label="", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
		lengthStoryValidation = forms.IntegerField(label="", widget=forms.TextInput(attrs={'class': 'form-control'}))

class saveStoryboard(forms.Form):
	nameStory = forms.CharField(max_length=100, label="", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
	lengthStoryboard = forms.IntegerField(label="", widget=forms.TextInput(attrs={'class': 'form-control'}))

class ChangeNameStoryboard(forms.Form):
	newNameStoryboard = forms.CharField(max_length=100, label="", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

class PublishStoryboard(forms.Form):
		messagetoryboard = forms.CharField(max_length=100, label="", required=True, widget=forms.Textarea(attrs={'class': 'form-control formPublishTextArea'}))