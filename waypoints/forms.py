from django import forms
from django.forms import Form, ModelForm, IntegerField, HiddenInput, ValidationError
from django.forms.fields import BooleanField
from .models import Waypoint, WaypointGroup, Entity
from logistics.models import Carrier, State, Country


class WaypointModelForm(ModelForm):
    """ ModelForm for Waypoint.

    This is the general model form for creating and updating waypoints.
    """

    class Meta:
        model = Waypoint
        fields = ('active',
                  'name',
                  'entity',
                  'time_open',
                  'time_close',
                  'lunch_break',
                  'lunch_time_start',
                  'lunch_time_end',
                  'open_saturday',
                  'saturday_time_start',
                  'saturday_time_end',
                  'open_holidays',
                  'holiday_time_start',
                  'holiday_time_end',
                  'contact_name',
                  'contact_last_name',
                  'contact_email',
                  'contact_phone',
                  'contact_phone_extension',
                  'latitude',
                  'longitude',
                  'carriers',
                  'external_id')

    id_waypoint = IntegerField(required=False, widget=HiddenInput())
    carriers = forms.ModelMultipleChoiceField(queryset=Carrier.objects.all(),
                                              required=False)
    country = forms.ModelChoiceField(queryset=Country.objects.all())
    entity = forms.ModelChoiceField(queryset=Entity.objects.all())
    holiday_time_end = forms.TimeField(widget=forms.TimeInput(format='%H:%M'),
                                       required=False)
    holiday_time_start = forms.TimeField(widget=forms.TimeInput(format='%H:%M'),
                                         required=False)
    lunch_time_end = forms.TimeField(widget=forms.TimeInput(format='%H:%M'),
                                     required=False)
    lunch_time_start = forms.TimeField(widget=forms.TimeInput(format='%H:%M'),
                                       required=False)
    saturday_time_end = forms.TimeField(widget=forms.TimeInput(format='%H:%M'),
                                        required=False)
    saturday_time_start = forms.TimeField(widget=forms.TimeInput(format='%H:%M'),
                                          required=False)
    state = forms.ModelChoiceField(queryset=State.objects.all())
    time_close = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    time_open = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            initial = kwargs.setdefault('initial', {})
            initial['carriers'] = [t.pk for t in kwargs['instance'].carriers.all()]
        super(WaypointModelForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        # https://docs.djangoproject.com/en/1.11/topics/forms/modelforms/#the-save-method
        # https://stackoverflow.com/questions/2216974/django-modelform-for-many-to-many-fields
        instance = ModelForm.save(self, False)
        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            instance.carriers.clear()
            for carrier in self.cleaned_data['carriers']:
                instance.carriers.add(carrier)
        self.save_m2m = save_m2m
        if commit:
            instance.save()
            self.save_m2m()

        return instance


class DeleteWaypointForm(Form):
    """ Form that is used to soft-delete (deactivate) a WaypointModel
    as well as the related user.

    """
    id_waypoint = IntegerField(widget=HiddenInput())

    def clean(self):
        """ Override clean data to validate the id corresponds
        to a real Waypoint.
        """
        self.cleaned_data = super(DeleteWaypointForm, self).clean()
        waypoint = Waypoint.objects.filter(pk=self.cleaned_data['id_waypoint'])
        if not waypoint:
            raise ValidationError('El punto de entrega no existe')
        return self.cleaned_data

    def save(self, *args, **kwargs):
        """ Override save to soft delete the waypoint.

        """
        waypoint = Waypoint.objects.get(pk=self.cleaned_data['id_waypoint'])
        waypoint.deleted = True
        waypoint.save()


class WaypointGroupModelForm(ModelForm):
    """ ModelForm for Waypoint.

    This is the general model form for creating and updating waypoints.
    """

    class Meta:
        model = WaypointGroup
        fields = ('active',
                  'name',
                  'entities')

    id_waypoint_group = IntegerField(required=False, widget=HiddenInput())
    entities = forms.ModelMultipleChoiceField(queryset=Entity.objects.all(),
                                              required=False)

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            initial = kwargs.setdefault('initial', {})
            initial['entities'] = [t.pk for t in kwargs['instance'].entities.all()]
        super(WaypointGroupModelForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        # https://docs.djangoproject.com/en/1.11/topics/forms/modelforms/#the-save-method
        # https://stackoverflow.com/questions/2216974/django-modelform-for-many-to-many-fields
        instance = ModelForm.save(self, False)
        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            instance.entities.clear()
            for entity in self.cleaned_data['entities']:
                instance.entities.add(entity)
        self.save_m2m = save_m2m
        if commit:
            instance.save()
            self.save_m2m()

        return instance


class DeleteWaypointGroupForm(Form):
    """ Form that is used to soft-delete (deactivate) a WaypointModel
    as well as the related user.

    """
    id_waypoint_group = IntegerField(widget=HiddenInput())

    def clean(self):
        """ Override clean data to validate the id corresponds
        to a real Waypoint.
        """
        self.cleaned_data = super(DeleteWaypointGroupForm, self).clean()
        waypoint_group = WaypointGroup.objects.filter(pk=self.cleaned_data['id_waypoint_group'])
        if not waypoint_group:
            raise ValidationError('El punto de entrega no existe')
        return self.cleaned_data

    def save(self, *args, **kwargs):
        """ Override save to soft delete the waypoint_group.

        """
        WaypointGroup.objects.get(pk=self.cleaned_data['id_waypoint_group']).delete()


class EntityModelForm(ModelForm):
    """ ModelForm for Waypoint.

    This is the general model form for creating and updating waypoints.
    """

    class Meta:
        model = Entity
        fields = ('name',)

    id_entity = IntegerField(required=False, widget=HiddenInput())

    def __init__(self, *args, **kwargs):
        super(EntityModelForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-control'


class DeleteEntityForm(Form):
    """ Form that is used to soft-delete (deactivate) a WaypointModel
    as well as the related user.

    """
    id_entity = IntegerField(widget=HiddenInput())

    def clean(self):
        """ Override clean data to validate the id corresponds
        to a real Waypoint.
        """
        self.cleaned_data = super(DeleteEntityForm, self).clean()
        entity = Entity.objects.filter(pk=self.cleaned_data['id_entity'])
        if not entity:
            raise ValidationError('La entidad no existe')
        return self.cleaned_data

    def save(self, *args, **kwargs):
        """ Override save to soft delete the entity.

        """
        Entity.objects.get(pk=self.cleaned_data['id_entity']).delete()
