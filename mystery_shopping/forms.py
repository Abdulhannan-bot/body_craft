from django import forms
from .models import MysteryShoppingOverview


class MysteryShoppingForm(forms.ModelForm):
    class Meta:
        model = MysteryShoppingOverview
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
            'cost_of_service': forms.TextInput(attrs={
                'class': "form-control",
                'required': "required",
                'type': "number"
            }),
            'invoice_number': forms.TextInput(attrs={
                'class': "form-control",
                'required': "required",
            }),
            'month_of_audit': forms.Select(attrs={
                'class': "form-control",
                'required': 'required',
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
            'payment_mode': forms.TextInput(attrs={
                'class': "form-control",
                'required': "required",
            }),
            'amount_redeemed': forms.TextInput(attrs={
                'class': "form-control",
                'required': "required",
                'type': "number"
            }),
            'contact_number_reached_for_appointment': forms.TextInput(attrs={
                'class': "form-control",
                'required': "required",
            }),
            'paid_in_cash': forms.TextInput(attrs={
                'class': "form-control",
                'required': "required",
                'type': "number"
            }),
            'service_availed_1': forms.TextInput(attrs={
                'class': "form-control",
                'required': "required",
            }),
            'service_availed_2': forms.TextInput(attrs={
                'class': "form-control",
            }),
            'service_availed_3': forms.TextInput(attrs={
                'class': "form-control",
            }),
            # 'auditor_completed': forms.boo(attrs={
            #     'class': "form-control",
            # }),
        }
