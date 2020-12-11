from django import forms
from .models import *
from ckeditor.fields import RichTextField

class ExampleForm(forms.ModelForm):
	name = forms.CharField(widget=forms.TextInput(), required=True, max_length=100)
	pwd = forms.CharField(widget=forms.TextInput(), required=True, max_length=20)
	bio = RichTextField()

	class Meta:
		model = User
		fields = ('name','pwd','bio')
    
    