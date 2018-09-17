from django import forms
from navigation.models import NavStore


class NavStoreForm(forms.ModelForm):
    class Meta:
        model=NavStore
        exclude=('c_date','id')
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'url':forms.URLInput(attrs={'class':'form-control'}),
            'remark':forms.TextInput(attrs={'class':'form-control'}),
        }