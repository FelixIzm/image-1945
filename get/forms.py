from django import forms

class UserForm(forms.Form):
    image_id = forms.CharField(label='ID')
