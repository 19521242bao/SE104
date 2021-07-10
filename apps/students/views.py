import csv
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.forms import widgets
from django.urls import reverse_lazy
from django.db.models import F, Sum
from apps.finance.models import Invoice
from apps.result.models import Result

from .models import Student, StudentBulkUpload


@login_required
def student_list(request):
  students = Student.objects.all()
  return render(request, 'students/student_list.html', {"students":students})

class StudentClassView(LoginRequiredMixin,ListView):
    model=Student
    template_name = "students/student_class.html"
    def get_queryset(self, *args, **kwargs):
        qs = super(StudentClassView, self).get_queryset()
        #qs = qs.order_by("-current_class")
        return qs
class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = "students/student_detail.html"
    all_score=0
    def get_context_data(self, **kwargs):
        context = super(StudentDetailView, self).get_context_data(**kwargs)
        context['payments'] = Invoice.objects.filter(student=self.object)
        context['results']=Result.objects.filter(student=self.object)
        #context['overall']=Result.objects.filter(student=self.object).aggregate(Sum('exam_score'))
        return context


class StudentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Student
    fields = '__all__'
    success_message = "New student successfully added."

    def get_form(self):
        '''add date picker in forms'''
        form = super(StudentCreateView, self).get_form()
        form.fields['date_of_birth'].widget = widgets.DateInput(
            attrs={'type': 'date'})
        form.fields['address'].widget = widgets.Textarea(attrs={'rows': 2})
        return form


class StudentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Student
    fields = '__all__'
    success_message = "Record successfully updated."

    def get_form(self):
        '''add date picker in forms'''
        form = super(StudentUpdateView, self).get_form()
        form.fields['date_of_birth'].widget = widgets.DateInput(
            attrs={'type': 'date'})
        #form.fields['date_of_admission'].widget = widgets.DateInput(attrs={'type': 'date'})
        form.fields['address'].widget = widgets.Textarea(attrs={'rows': 2})
        #form.fields['others'].widget = widgets.Textarea(attrs={'rows': 2})
        form.fields['passport'].widget = widgets.FileInput()
        return form


class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    success_url = reverse_lazy('student-list')


class StudentBulkUploadView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = StudentBulkUpload
    template_name = 'students/students_upload.html'
    fields = ['csv_file']
    success_url = '/student/list'
    success_message = 'Successfully uploaded students'

@login_required
def downloadcsv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="student_template.csv"'

    writer = csv.writer(response)
    writer.writerow(['registration_number', 'surname',
                     'firstname', 'other_names', 'gender', 'parent_number', 'address', 'current_class'])

    return response
