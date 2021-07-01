from django import forms
from django.forms import ModelForm, modelformset_factory

from .models import SiteConfig, AcademicTerm, AcademicSession, StudentClass, Subject
from apps.students.models import Student
SiteConfigForm = modelformset_factory(SiteConfig, fields=('key', 'value',), extra=0)

class AcademicSessionForm(ModelForm):
  prefix = 'Academic Session'
  class Meta:
    model = AcademicSession
    fields = ['name','current']

class AcademicTermForm(ModelForm):
  prefix = 'Academic Term'
  class Meta:
    model = AcademicTerm
    fields = ['name','current']

class SubjectForm(ModelForm):
  prefix = 'Subject'
  class Meta:
    model = Subject
    fields = ['name']

class StudentClassForm(ModelForm):
  prefix = 'Class'
  class Meta:
    model = StudentClass
    fields = ['name']

class CurrentSessionForm(forms.Form):
  current_session = forms.ModelChoiceField(queryset=AcademicSession.objects.all(), help_text='Click <a href="/session/create/?next=current-session/">here</a> to add new session')
  current_term = forms.ModelChoiceField(queryset=AcademicTerm.objects.all(), help_text='Click <a href="/term/create/?next=current-session/">here</a> to add new term')
class CreateStudent_ClassForm(forms.Form):
  session = forms.ModelChoiceField(queryset=AcademicSession.objects.all())
  term = forms.ModelChoiceField(queryset=AcademicTerm.objects.all())
  current_class=forms.ModelChoiceField(queryset=StudentClass.objects.all())

#EditResults = modelformset_factory(Student, fields=('current_class'), extra=0, can_delete=True)
