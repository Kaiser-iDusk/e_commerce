from django.utils import timezone
from zoneinfo import ZoneInfo
from datetime import timedelta
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Address
from shop.models import ReturnRequest

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        try:
            from phonenumber_field.phonenumber import PhoneNumber
            parsed_number = PhoneNumber.from_string(phone_number)
            if not parsed_number.is_valid():
                raise forms.ValidationError('Invalid phone number.')
            if CustomUser.objects.filter(phone_number=parsed_number).exists():
                raise forms.ValidationError('This phone number is already in use.')
            return parsed_number
        except Exception:
            raise forms.ValidationError('Invalid phone number format.')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already in use.')
        return email

class TwoFactorForm(forms.Form):
    otp = forms.CharField(max_length=6, min_length=6, required=True, label='Enter OTP')

class AddressForm(forms.ModelForm):
    use_existing = forms.BooleanField(
        required=False,
        label='Use Existing Address',
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox', 'id': 'use-existing'}),
    )
    existing_address = forms.ModelChoiceField(
        queryset=Address.objects.none(),
        required=False,
        label='Select Address',
        widget=forms.Select(attrs={'class': 'form-select mt-1 block w-full', 'id': 'existing-address'}),
    )

    class Meta:
        model = Address
        fields = ['street', 'city', 'state', 'zip_code', 'country']
        widgets = {
            'street': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full'}),
            'city': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full'}),
            'state': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full'}),
            'country': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['existing_address'].queryset = Address.objects.filter(user=user)
        if not self.fields['existing_address'].queryset.exists():
            self.fields['use_existing'].initial = False
            self.fields['use_existing'].widget.attrs['disabled'] = True
        else:
            self.fields['existing_address'].required = False

    def clean(self):
        cleaned_data = super().clean()
        use_existing = cleaned_data.get('use_existing')
        existing_address = cleaned_data.get('existing_address')

        if use_existing:
            if not existing_address:
                raise forms.ValidationError('Please select an existing address.')
            # Make new address fields optional when using existing address
            for field in ['street', 'city', 'state', 'zip_code', 'country']:
                self.fields[field].required = False
        else:
            # Ensure new address fields are filled
            for field in ['street', 'city', 'state', 'zip_code', 'country']:
                if not cleaned_data.get(field):
                    self.add_error(field, 'This field is required when not using an existing address.')
        return cleaned_data

class DeliveryTimeForm(forms.Form):
    preferred_delivery_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-input mt-1 block w-full'}),
        label='Preferred Delivery Time'
    )

    def clean_preferred_delivery_time(self):
        delivery_time_naive = self.cleaned_data['preferred_delivery_time']  # naive datetime from input
        india_tz = ZoneInfo("Asia/Kolkata")

        # Treat submitted time as India local time
        delivery_time = delivery_time_naive.replace(tzinfo=india_tz)

        # Minimum allowed = now in India + 1 minute
        min_allowed = timezone.now().astimezone(india_tz) + timedelta(minutes=1)
        if delivery_time <= min_allowed:
            raise forms.ValidationError('Delivery time must be at least 1 minute in the future (India time).')

        return delivery_time

class ReturnRequestForm(forms.ModelForm):
    class Meta:
        model = ReturnRequest
        fields = ['description']
        widgets = {'description': forms.Textarea(attrs={'rows': 4})}