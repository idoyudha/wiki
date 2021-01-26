from django import forms

class NameForm(forms.Form):
    search = forms.CharField(label='q', max_length=100)