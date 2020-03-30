from django import forms

class FormSelectId(forms.Form):
    _id = forms.CharField(label='ID image', initial='123', required=False, widget=forms.TextInput(attrs={'class':'myfield'}))
    #path_dir = forms.CharField(label='path', initial='', required=False, widget=forms.TextInput(attrs={'class':'myfield'}))