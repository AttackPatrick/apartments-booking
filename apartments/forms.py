from django import forms
from .models import ApartmentAddress
from ukpostcodeutils import validation

class ApartmentAddressForm(forms.ModelForm):
    def clean_postcode(self):
        postcode = self.cleaned_data.get('postcode')
        print(validation.is_valid_postcode(postcode))
        if not validation.is_valid_postcode(postcode):
            raise forms.ValidationError('postcode is not valid: e.g. B228MR (with no white spaces)!')
        else:
            return postcode

    class Meta:
        model = ApartmentAddress
        fields = '__all__'
        