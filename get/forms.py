from django import forms

class UserForm(forms.Form):
    image_id = forms.CharField(label='ID',initial='1234',widget= forms.TextInput(attrs={'class':'myfield'}))
#,widget= forms.TextInput(attrs={'class':'field-style','id':'some_id'})