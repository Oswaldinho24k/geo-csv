from django.contrib.auth import get_user_model
from django.forms import Form, ModelForm, HiddenInput, IntegerField, ValidationError
from .models import Client


class UserModelForm(ModelForm):
    """ ModelForm for Users.

    This is the general model form for creating and updating users.
    """

    id_user = IntegerField(required=False, widget=HiddenInput())

    class Meta:
        model = get_user_model()
        fields = ['username',
                  'first_name',
                  'last_name',
                  'email']
        labels = {
            'username': ('Nombre de Usuario'),
            'first_name': ('Nombres'),
            'last_name': ('Apellidos'),
            'email': ('Email')
        }

    def __init__(self, *args, **kwargs):
        super(UserModelForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ClientModelForm(ModelForm):
    """ Model form for Client

        This is the general form for updating a Client.
    """

    class Meta:
        model = Client
        fields = ('active',
                  'groups',
                  'commercial_contact_name',
                  'commercial_contact_email',
                  'commercial_contact_phone',
                  'legal_business_name',
                  'rfc',
                  'billing_address',
                  'billing_email',
                  'billing_phone',
                  'finance_contact_name',
                  'finance_contact_email',
                  'logistics_contact_name',
                  'logistics_contact_email',
                  'billing_conditions',
                  'ecommerce_platform')

        labels = {
            'active': ('Activo')
        }

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            initial = kwargs.setdefault('initial', {})
            initial['groups'] = [g.pk for g in kwargs['instance'].groups.all()]
        super(ClientModelForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'active':
                field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True, form_user=None):
        # https://docs.djangoproject.com/en/1.11/topics/forms/modelforms/#the-save-method
        # https://stackoverflow.com/questions/2216974/django-modelform-for-many-to-many-fields
        instance = ModelForm.save(self, False)
        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            instance.groups.clear()
            for group in self.cleaned_data['groups']:
                instance.groups.add(group)
        self.save_m2m = save_m2m

        if form_user is not None:
            instance.user = form_user

        if commit:
            instance.save()
            self.save_m2m()

        return instance


class DeleteClientForm(Form):
    """ Form that is used to soft-delete (deactivate) a ClientModel
    as well as the related user.

    """
    id_client = IntegerField(widget=HiddenInput())

    def clean(self):
        """ Override clean data to validate the id corresponds
        to a real Client.
        """
        self.cleaned_data = super(DeleteClientForm, self).clean()
        client = Client.objects.filter(pk=self.cleaned_data['id_client'])
        if not client:
            raise ValidationError('El cliente no existe')
        return self.cleaned_data

    def save(self, *args, **kwargs):
        """ Override save to soft delete the client.

        """
        client = Client.objects.get(pk=self.cleaned_data['id_client'])
        client.active = False
        client.save()
