from django import forms
from django.core.mail import send_mail
import logging
from . import models
from django.forms import inlineformset_factory
from . import widgets

logger = logging.getLogger(__name__)


class ContactForm(forms.Form):
    name = forms.CharField(label='Your name', max_length=100)
    message = forms.CharField(max_length=600, widget=forms.Textarea)

    def send_mail(self):
        logger.info("Sending email to customer service")
        message = "From: {0}\n{1}".format(
            self.cleaned_data["name"],
            self.cleaned_data["message"],
        )
        send_mail(
            "Site message",
            message,
            "site@booktime.domain",
            ["customerservice@booktime.domain"],
            fail_silently=False,
        )


BasketLineFormSet = inlineformset_factory(
    models.Basket,
    models.BasketLine,
    fields=("quantity",),
    extra=0,
    widgets={"quantity": widgets.PlusMinusNumberInput()},
)


class AddressSelectionForm(forms.Form):
    billing_address = forms.ModelChoiceField(
        queryset=None)
    shipping_address = forms.ModelChoiceField(
        queryset=None)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        queryset = models.Address.objects.filter(user=user)
        self.fields['billing_address'].queryset = queryset
        self.fields['shipping_address'].queryset = queryset
