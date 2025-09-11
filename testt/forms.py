from django import forms
from .models import Page, Test, SnippetVariant
from django.forms import modelformset_factory


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ["url"]


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ["start_date", "end_date"]


class SnippetVariantForm(forms.ModelForm):
    class Meta:
        model = SnippetVariant
        fields = ["title", "description", "variant_label"]


SnippetVariantFormSet = modelformset_factory(
    SnippetVariant,
    form=SnippetVariantForm,
    extra=2,  # show at least 2 empty forms
    min_num=2,  # require at least 2
    validate_min=True
)
