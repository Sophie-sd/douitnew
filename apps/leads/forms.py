import re

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Lead


class LeadForm(forms.ModelForm):
    UA_PHONE_RE = re.compile(r"^\+380\d{9}$")

    website = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"tabindex": "-1", "autocomplete": "off"}),
        label="",
    )
    utm_source = forms.CharField(required=False, widget=forms.HiddenInput)
    utm_medium = forms.CharField(required=False, widget=forms.HiddenInput)
    utm_campaign = forms.CharField(required=False, widget=forms.HiddenInput)
    source_url = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Lead
        fields = ["name", "contact", "project_type", "comment"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": _("Ваше ім'я"), "autocomplete": "name"}),
            "contact": forms.TextInput(
                attrs={
                    "placeholder": "+38(0__)___-__-__",
                    "autocomplete": "tel",
                    "type": "tel",
                    "data-phone-ua": "",
                }
            ),
            "project_type": forms.Select(),
            "comment": forms.Textarea(attrs={"placeholder": _("Розкажіть про проєкт (необов'язково)"), "rows": 3}),
        }

    def clean_contact(self):
        value = self.cleaned_data["contact"].strip()
        digits = re.sub(r"\D", "", value)

        if digits.startswith("0"):
            digits = "38" + digits
        elif digits.startswith("80"):
            digits = "3" + digits

        normalized = f"+{digits}"
        if not self.UA_PHONE_RE.match(normalized):
            raise forms.ValidationError(
                _("Введіть коректний український номер телефону.")
            )
        return normalized

    def clean_project_type(self):
        return self.cleaned_data.get("project_type") or Lead.ProjectType.OTHER


class ModalLeadForm(forms.ModelForm):
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            "placeholder": "+380 XX XXX XXXX",
            "autocomplete": "tel",
            "data-phone-ua": "",
            "type": "tel",
        }),
        label=_("Телефон"),
    )
    website = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"tabindex": "-1", "autocomplete": "off"}),
        label="",
    )
    utm_source = forms.CharField(required=False, widget=forms.HiddenInput)
    utm_medium = forms.CharField(required=False, widget=forms.HiddenInput)
    utm_campaign = forms.CharField(required=False, widget=forms.HiddenInput)
    source_url = forms.CharField(required=False, widget=forms.HiddenInput)
    quiz_features = forms.CharField(required=False, widget=forms.HiddenInput)
    quiz_pages = forms.CharField(required=False, widget=forms.HiddenInput)
    quiz_deadline = forms.CharField(required=False, widget=forms.HiddenInput)
    quiz_budget = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Lead
        fields = ["name", "project_type", "quiz_features", "quiz_pages",
                  "quiz_deadline", "quiz_budget"]
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": _("Ваше ім'я"),
                "autocomplete": "name",
            }),
            "project_type": forms.Select(),
        }

    UA_PHONE_RE = re.compile(r"^\+?3?8?0\d{9}$")

    def clean_phone(self):
        raw = re.sub(r"[\s\-\(\)]", "", self.cleaned_data["phone"])
        if not self.UA_PHONE_RE.match(raw):
            raise forms.ValidationError(
                _("Введіть коректний український номер: +380 XX XXX XXXX")
            )
        if not raw.startswith("+"):
            raw = "+" + raw
        if raw.startswith("+0"):
            raw = "+380" + raw[2:]
        elif raw.startswith("+80"):
            raw = "+380" + raw[3:]
        return raw

    def clean_project_type(self):
        return self.cleaned_data.get("project_type") or Lead.ProjectType.OTHER

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.contact = self.cleaned_data["phone"]
        if commit:
            instance.save()
        return instance
