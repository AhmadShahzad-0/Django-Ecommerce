from django import forms
from . models import ShippingAddress

# Create Forms Here
class ShippingForm(forms.ModelForm):
    shipping_full_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Full Name'}), required=True)
    shipping_phone = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Contact Number'}), required=True)
    shipping_email = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}), required=True)
    shipping_address1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address1'}), required=True)
    shipping_address2 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address2'}), required=False)
    shipping_city = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}), required=True)
    shipping_state = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}), required=True)
    shipping_zipcode = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zipcode'}), required=True)
    shipping_country = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country'}), required=True)

    class Meta:
        model = ShippingAddress
        fields = ['shipping_full_name', 'shipping_phone', 'shipping_email', 'shipping_address1', 'shipping_address2', 'shipping_city', 'shipping_state', 'shipping_zipcode', 'shipping_country']

        exclude = ['user']

class PaymentForm(forms.Form):
    card_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Account Name'}), required=False)
    card_number = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Account Number'}), required=False)
    # card_exp_date = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Card Expiry'}), required=True)
    # card_cvv_number = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'CVV Number'}), required=True)
    # card_address = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Card Address'}), required=False)
    # card_city = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Card City'}), required=True)
    # card_state = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Card State'}), required=True)
    # card_zipcode = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Card Zipcode'}), required=True)
    # card_country = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Card Country'}), required=True)