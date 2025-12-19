from django import forms
from .models import Deployment


class DeployForm(forms.ModelForm):
    class Meta:
        model = Deployment
        fields = ['customer_name', 'service_id', 'region', 'manufacturer',
                  'model_type', 'serial_number']  # отстранивме mac_address

        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Customer name'
            }),
            'service_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Service ID'
            }),
            'region': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_region'
            }),
            'manufacturer': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_manufacturer'
            }),
            'model_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'serial_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ABC1234D5E6',
                'id': 'id_serial_number'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        manufacturer = cleaned_data.get('manufacturer')
        serial_number = cleaned_data.get('serial_number')

        # Валидација за Serial/MAC
        if manufacturer == 'cisco' and not serial_number:
            raise forms.ValidationError("Serial Number е задолжителен за Cisco уреди!")

        if manufacturer == 'huawei' and not serial_number:
            raise forms.ValidationError("MAC Address е задолжителен за Huawei уреди!")

        return cleaned_data
