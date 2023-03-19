from django import forms
from .models import CorporateAuditOverview


class CorporateAuditForm(forms.ModelForm):
    class Meta:
        model = CorporateAuditOverview
        fields = '__all__'
        exclude = ['added_on', 'added_by']

        widgets = {
            'center': forms.Select(attrs={
                'class': "form-control",
                'required': 'required',
            }),
            'shopper_name': forms.TextInput(attrs={
                'class': "form-control",
                'required': 'required',
            }),
            'mobile': forms.TextInput(attrs={
                'class': "form-control",
                'required': "required",
            }),
            'email': forms.TextInput(attrs={
                'class': "form-control",
                'required': "required",
            }),
            'gender': forms.TextInput(attrs={
                'class': "form-control",
                'required': "required",
            }),
            'invoice_number': forms.TextInput(attrs={
                'class': "form-control",
                'required': "required",
            }),
            'date': forms.DateInput(attrs={
                'class': "form-control ",
                'required': "required",
                'type': "date",
            }),
            'start_time': forms.TimeInput(attrs={
                'class': "form-control",
                'required': "required",
                'type': "time",
            }),
            'end_time': forms.TimeInput(attrs={
                'class': "form-control",
                'required': "required",
                'type': "time",
            }),
            'contact_number_reached_for_appointment': forms.TextInput(attrs={
                'class': "form-control",
                'required': "required",
            }),
        }
