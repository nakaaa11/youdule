from django import forms
from .models import UserInfo
 
class UserForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ('name','age')
        labels={
           'name':'名前',
           'age': '年齢'
           }
    
class Form(forms.Form):
    text = forms.CharField(label="文字")