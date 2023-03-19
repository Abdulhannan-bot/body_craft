from django import forms
from .models import ExtendedZenotiEmployeesData, EmployeeRoster, ExtendedZenotiCenterData


class ExtendedZenotiDataForm(forms.ModelForm):
    class Meta:
        model = ExtendedZenotiEmployeesData
        fields = '__all__'
        exclude = ['zenoti_data']

        widgets = {
            'associated_center': forms.SelectMultiple(attrs={
                'class': "form-control select2",
                'multiple': "multiple",
                'style': "height: 36px;width: 100%;",
                'required': 'required',
            }),
            'associated_role': forms.SelectMultiple(attrs={
                'class': "form-control select2",
                'multiple': "multiple",
                'style': "height: 36px;width: 100%;",
                # 'required': "required"
            }),
            'office_start_time': forms.TimeInput(attrs={
                'class': "form-control",
                'required': "required",
                'type': 'time',
            }),
            'office_end_time': forms.TimeInput(attrs={
                'class': "form-control",
                'required': "required",
                'type': 'time',
            }),
            'week_off': forms.SelectMultiple(attrs={
                'class': "form-control select2",
                'multiple': "multiple",
                'style': "height: 36px;width: 100%;",
                'required': "required",
            }),
            'password': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'is_manager': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'onchange': "pass_required(this);"
            })
        }


class EmployeeRosterForm(forms.ModelForm):
    class Meta:
        model = EmployeeRoster
        fields = '__all__'

        widgets = {
            'center': forms.Select(attrs={
                'class': "form-control",
                'required': 'required',
            }),
            'employee': forms.Select(attrs={
                'class': "form-control",
                'required': 'required',
            }),
            'associated_role': forms.Select(attrs={
                'class': "form-control",
                'required': "required",
            }),
            'appoint_date': forms.DateInput(attrs={
                'class': "form-control ",
                'required': "required",
                'type': "date",
            }),
            'office_start_time': forms.TimeInput(attrs={
                'class': "form-control",
                'required': "required",
                'type': "time",
            }),
            'office_end_time': forms.TimeInput(attrs={
                'class': "form-control",
                'required': "required",
                'type': "time",
            }),
        }


class ExtendedZenotiCenterDataForm(forms.ModelForm):
    class Meta:
        model = ExtendedZenotiCenterData
        fields = '__all__'
        exclude = ['zenoti_data']

        widgets = {
            'closed_on': forms.SelectMultiple(attrs={
                'class': "form-control select2",
                'multiple': "multiple",
                'style': "height: 36px;width: 100%;",
            }),
            'opening_time': forms.TimeInput(attrs={
                'class': "form-control",
                'required': "required",
                'type': 'time',
            }),
            'closing_time': forms.TimeInput(attrs={
                'class': "form-control",
                'required': "required",
                'type': 'time',
            }),
            'position': forms.SelectMultiple(attrs={
                'class': "form-control select2",
                'multiple': "multiple",
                'style': "height: 36px;width: 100%;",
            }),
            'center_status': forms.Select(attrs={
                'class': "form-control",
                'required': 'required',
            }),
        }
