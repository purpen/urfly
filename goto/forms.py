from django import forms

class LinkForm(forms.Form):
	link = forms.CharField(255)