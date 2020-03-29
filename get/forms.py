from django import forms

class UserForm(forms.Form):
    image_id = forms.CharField(label='ID', initial='1234', widget=forms.TextInput(attrs={'class':'myfield'}))
    excel = forms.BooleanField(required=False)
#,widget= forms.TextInput(attrs={'class':'field-style','id':'some_id'})
class FormSelectDir(forms.Form):
    #path_dir = forms.FilePathField(path='/tmp',allow_files=False,allow_folders=True)
    path_dir = forms.CharField(label='path', initial='', required=False, widget=forms.TextInput(attrs={'class':'myfield'}))