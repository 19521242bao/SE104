from django import forms
from django.forms import modelformset_factory, BaseModelFormSet

from apps.corecode.models import AcademicSession, AcademicTerm, Subject,StudentClass

from .models import Result

class CreateResults(forms.Form):
  session = forms.ModelChoiceField(queryset=AcademicSession.objects.all())
  term = forms.ModelChoiceField(queryset=AcademicTerm.objects.all())
  subjects = forms.ModelMultipleChoiceField(
      queryset=Subject.objects.all(), widget=forms.CheckboxSelectMultiple)
EditResults = modelformset_factory(Result, fields=('test_score', 'exam_score'), extra=0, can_delete=True)

class CreateResultCLass(forms.Form):
    session = forms.ModelChoiceField(queryset=AcademicSession.objects.all())
    term = forms.ModelChoiceField(queryset=AcademicTerm.objects.all())
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(), widget=forms.CheckboxSelectMultiple)
    current_class=forms.ModelChoiceField(queryset=StudentClass.objects.all())
class GetResutlSubjectForm(forms.Form):
    subjects =forms.ModelChoiceField(queryset=Subject.objects.all())
    session = forms.ModelChoiceField(queryset=AcademicSession.objects.all())
    term = forms.ModelChoiceField(queryset=AcademicTerm.objects.all())

