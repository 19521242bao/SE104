from django import forms
from django.forms import ModelForm, modelformset_factory

from .models import  Student
from ..corecode.models import SiteConfig

SiteConfigForm = modelformset_factory(SiteConfig, fields=('key', 'value',), extra=0)
