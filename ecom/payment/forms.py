from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
      
      shipping_full_name = forms.CharField(label="Full_name", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Full_name'}), required=True)
      shipping_email = forms.CharField(label="Email", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}), required=True)
      shipping_address1 = forms.CharField(label="Address1", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address1'}), required=True)
      shipping_address2 = forms.CharField(label="Address2", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address2'}), required=False)
      shipping_city = forms.CharField(label="City", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}), required=True)
      shipping_state = forms.CharField(label="State", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}), required=False)
      shipping_zipcode = forms.CharField(label="Zipcode", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zipcode'}), required=False)
      shipping_country = forms.CharField(label="Country", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country'}), required=False)
	
      
	   
      class Meta:
        model = ShippingAddress
        fields = ('shipping_full_name', 'shipping_email','shipping_address1','shipping_address2','shipping_city','shipping_state', 'shipping_zipcode', 'shipping_country')

        exclude =['user' ,]

class PaymentForm(forms.Form):
    
    card_name = forms.CharField(label="Card Name", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Card Name'}), required=True)
    card_number = forms.CharField(label="Card Number", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Card Number'}), required=True)
    card_exp_date = forms.CharField(label="Expiry Date", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Expiry Date'}), required=True)
    card_cvv_number = forms.CharField(label="Cvv Number", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Cvv Number'}), required=True)
    card_address1 = forms.CharField(label="Address1", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address1'}), required=True)
    card_address2 = forms.CharField(label="Address2", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address2'}), required=False)
    card_city = forms.CharField(label="City", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}), required=True)
    card_state = forms.CharField(label="State", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}), required=True)
    card_zipcode = forms.CharField(label="Zipcode", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zipcode'}), required=True)
    card_country = forms.CharField(label="Country", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country'}), required=True)


