#!/usr/bin/env python
from django import forms
from django.forms import Select, TextInput, Textarea
from cmdb.models import *


class AssetForm(forms.ModelForm):
    label = forms.CharField(label='标签', widget=forms.TextInput(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.fields['label'].initial = ','.join([i.name for i in instance.tags.all()])

    class Meta:
        model = Asset
        exclude = ('id', 'tags')
        widgets = {
            'asset_type': Select(attrs={'class': 'form-control'}),
            'name': TextInput(attrs={'class': 'form-control'}),
            'sn': TextInput(attrs={'class': 'form-control'}),
            'status': Select(attrs={'class': 'form-control'}),
            'business_unit': Select(attrs={'class': 'form-control'}),
            'manufacturer': Select(attrs={'class': 'form-control'}),
            'manage_ip': TextInput(attrs={'class': 'form-control'}),
            'admin': Select(attrs={'class': 'form-control'}),
            'idc': Select(attrs={'class': 'form-control'}),
            'contract': Select(attrs={'class': 'form-control'}),
            'purchase_day': TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', }),
            'expire_day': TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', }),
            'approved_by': Select(attrs={'class': 'form-control'}),
            'price': TextInput(attrs={'class': 'form-control'}),
            'memo': Textarea(attrs={'class': 'form-control'}),
            'c_time': TextInput(attrs={'class': 'form-control'}),
            'm_time': TextInput(attrs={'class': 'form-control'}),
        }

    def clean_label(self):
        label = self.cleaned_data.get('label', '')
        label_list = [i for i in label.split(',') if i]
        if len(label_list) > 5:
            raise forms.ValidationError('最多5个标签，当前%s个' % len(label))
        else:
            for i in label_list:
                if label_list.count(i) > 1:
                    raise forms.ValidationError('有重复的标签')
        return label


class IDCForm(forms.ModelForm):
    class Meta:
        model = IDC
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.model._meta.fields:
            if field.name == 'id':
                continue
            self.fields[field.name].widget.attrs = {"class": "form-control", }


class ServerForm(forms.ModelForm):
    class Meta:
        model = Server
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.model._meta.fields:
            if field.name == 'id':
                continue
            self.fields[field.name].widget.attrs = {"class": "form-control", }


class NetworkForm(forms.ModelForm):
    class Meta:
        model = NetworkDevice
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.model._meta.fields:
            if field.name == 'id':
                continue
            self.fields[field.name].widget.attrs = {"class": "form-control", }


class SoftwareForm(forms.ModelForm):
    class Meta:
        model = Software
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.model._meta.fields:
            if field.name == 'id':
                continue
            self.fields[field.name].widget.attrs = {"class": "form-control", }


class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.model._meta.fields:
            if field.name == 'id':
                continue
            self.fields[field.name].widget.attrs = {"class": "form-control", }

class BusinessUnitForm(forms.ModelForm):
    class Meta:
        model = BusinessUnit
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.model._meta.fields:
            if field.name == 'id':
                continue
            self.fields[field.name].widget.attrs = {"class": "form-control", }

class ContractUnitForm(forms.ModelForm):
    class Meta:
        model=Contract
        exclude=['c_day','m_day']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.model._meta.fields:
            if field.name == 'id' or field.name in self.Meta.exclude:
                continue
            self.fields[field.name].widget.attrs = {"class": "form-control", }