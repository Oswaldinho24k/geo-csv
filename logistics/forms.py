from django.forms import ModelForm
from .models import Address


class AddressModelForm(ModelForm):
    """ ModelForm for Address.

    This is the general model form for creating and updating addresses.
    """

    class Meta:
        model = Address
        fields = ('line_one',
                  'line_two',
                  'neighborhood',
                  'city',
                  'postal_code')

    def __init__(self, *args, **kwargs):
        super(AddressModelForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
