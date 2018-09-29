from django import forms

class APIform(forms.Form):
	g_username = forms.CharField(max_length=30, label='GitHub Username', required = False)