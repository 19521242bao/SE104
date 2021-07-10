from collections import Counter

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.views.generic import ListView

from apps.corecode.models import AcademicSession, AcademicTerm,StudentClass
from apps.students.models import Student

from .models import Result
from .forms import CreateResults, EditResults,CreateResultCLass,GetResutlSubjectForm

ListView
@login_required
def create_result(request):
  students = Student.objects.all()
  if request.method == 'POST':

    #after visiting the second page
    if 'finish' in request.POST:
      form = CreateResults(request.POST)
      if form.is_valid():
        subjects = form.cleaned_data['subjects']
        session = form.cleaned_data['session']
        term = form.cleaned_data['term']
        students = request.POST['students']
        results = []
        for student in students.split(','):
          stu = Student.objects.get(pk=student)
          if stu.current_class:
            for subject in subjects:
              check = Result.objects.filter(session=session, term=term,current_class=stu.current_class,subject=subject, student=stu).first()
              if not check:
                results.append(
                    Result(
                        session=session,
                        term=term,
                        current_class=stu.current_class,
                        subject=subject,
                        student=stu
                    )
                )

        Result.objects.bulk_create(results)
        return redirect('edit-results')

    #after choosing students
    id_list = request.POST.getlist('students')
    if id_list:
      form = CreateResults(initial={"session": request.current_session, "term":request.current_term})
      studentlist = ','.join(id_list)
      return render(request, 'result/create_result_page2.html', {"students": studentlist, "form": form, "count":len(id_list)})
    else:
      messages.warning(request, "You didnt select any student.")
  return render(request, 'result/create_result.html', {"students": students})
@login_required
def add_score(request):
  class_list=StudentClass.objects.all()
  if request.method == 'POST':
    if 'finish' in request.POST:
      form = EditResults(request.POST)

      if form.is_valid():
        form.save()
        messages.success(request, 'Results successfully updated')
        return redirect('view-results')
    else:
      if "current_class" in request.POST:

        class_name = request.POST['current_class']
        results = Result.objects.filter(
            session=request.current_session, term=request.current_term,current_class=class_name)
        form = EditResults(queryset=results)
        return render(request, 'result/edit_results2.html', {"formset": form})
      class_id=request.POST.getlist('current_class')
    print(class_id)

    if class_id:
      form=CreateResultCLass(initial={"session": request.current_session, "term":request.current_term})
      class_select=','.join(class_id)
      return render(request, 'result/edit_results2.html',
                    {"current_class": class_select, "form": form, "count": len(class_id)})
    else:
        messages.warning(request, "You didnt select any class.")
  return render(request, 'result/class_list.html', {"class_list": class_list})

def edit_results(request):

  if request.method == 'POST':
    form = EditResults(request.POST)

    if form.is_valid():
      form.save()
      messages.success(request, 'Results successfully updated')
      return redirect('edit-results')

  else:
    results = Result.objects.filter(
        session=request.current_session, term=request.current_term)
    form = EditResults(queryset=results)
  return render(request, 'result/edit_results.html', {"formset": form})

@login_required
def all_results_view_class(request):
  results = Result.objects.filter(
    session=request.current_session, term=request.current_term)
  bulk = {}

  for result in results:
    test_total = 0
    exam_total = 0
    subjects = []
    for subject in results:
      if subject.student == result.student:
        subjects.append(subject)
        subject.test_score = float(subject.test_score)
        subject.exam_score = float(subject.exam_score)
        test_total = (test_total + subject.test_score)
        exam_total = (exam_total + subject.exam_score)
    test_total = test_total / len(subjects)
    exam_total = exam_total / len(subjects)
    bulk[result.student.id] = {
      "student": result.student,
      "subjects": subjects,
      "test_total": test_total,
      "exam_total": exam_total,
      "total_total": round((test_total + exam_total) / 2, 2)
    }

  context = {
    "results": bulk
  }
  return render(request, 'result/all_results.html', context)


def score_grade(score):
  if score <= 10 and score >= 8:
    return 'Giỏi'
  elif score < 8 and score >= 6.5:
    return 'Khá'
  elif score < 6.5 and score >= 5:
    return 'Trung Bình'
  elif score >= 0 and score < 5:
    return 'Không Đạt'
  else:
    return "Invalid Score"

@login_required
def all_results_view(request):
  results = Result.objects.filter(
    session=request.current_session, term=request.current_term)
  bulk = {}

  def find_student(arr, target):
    for i in range(1, len(arr)):
      if arr[i][0] == target:
        return i
    return -1

  grade = []
  t = len(results)
  classlist = []  # Ten cac lop
  grading_class = [["", 0, 0, 0, 0]]  # [Ten class, A, B, C, D]
  std = [["example", 0, 0, "A", "class"]]  # [Ten hoc sinh, Diem Trung Binh, cnt , grading, Class]

  for result in results:
    test_class = 0
    exam_class = 0
    total_average = 0
    total_total = 0
    class_member = []
    if result.current_class not in classlist:
      classlist.append(result.current_class)
      grading_class.append([classlist[-1], 0, 0, 0, 0])
      for student in results:
        grade.append(result.current_class)
        if student.current_class == result.current_class:
          class_member.append(student.student)
          if find_student(std, student.student) == -1 or len(std) == 1:
            std.append([student.student, 0, 0, "", student.current_class])
          exam_class += student.exam_score
          test_class += student.test_score
          total_total = (student.exam_score + student.test_score) / 2
          position_student_in_std = find_student(std, student.student)
          std[position_student_in_std][1] += total_total
          std[position_student_in_std][2] += 1
          if std[position_student_in_std][2] == 2:
            std[position_student_in_std][2] = 1
            std[position_student_in_std][1] /= 2

  for i in range(1, len(std)):
    std[i][3] = score_grade(std[i][1])
    for j in range(1, len(grading_class)):
      if std[i][-1] == grading_class[j][0]:
        grading_class[j][2] += 1
        if std[i][3] == "Giỏi":
          grading_class[j][1] += 1

        if std[i][3] == "Khá":
          grading_class[j][1] += 1
        if std[i][3] == "Trung Bình":
          grading_class[j][1] += 1

  x = len(std)

  for i in range(1, len(grading_class)):
    if grading_class[i][2] == 0:
      percent=0
    else:
      percent=int((grading_class[i][1]/(grading_class[i][2]))*100)
    bulk[grading_class[i][0]] = {
      "name_class": grading_class[i][0],
      "term": request.current_term,
      "percent": percent,
      "good": grading_class[i][1],
      "SL":grading_class[i][2]
    }
  context = {
    "results": bulk
  }
  return render(request, 'result/all_results_class.html', context)
def all_result_view_subject(request):
  bulk = {}
  if request.method == 'POST':

    form = GetResutlSubjectForm(request.POST)
    if form.is_valid():

      subjects = form.cleaned_data['subjects']
      term=form.cleaned_data['term']
      session=form.cleaned_data['session']
      results=Result.objects.filter(term=term,session=session,subject=subjects)
      list_class=list(results.values_list('current_class', flat=True).distinct())
      name_class=""
      for id_class in list_class:
        print(id_class)
        number_class=0
        good_member=0

        for result in results:
          if result.current_class.id==id_class:
            name_class=result.current_class
            number_class+=1
            score_student=(result.total_score())
            if score_student>=5:
              good_member+=1
          print(subjects)
        bulk[id_class] = {
          "name_subject":subjects,
          "name_class": name_class,
          "term": request.current_term,
          "percent": int(good_member/number_class*100),
          "good": good_member,
          "SL":number_class
        }
      print(bulk)
      context = {
          "results": bulk,
          "form":form
        }



      return render(request, 'result/result_subject.html', context)
  form = GetResutlSubjectForm(initial={"session": request.current_session, "term": request.current_term})
  return render(request, 'result/result_subject.html', {"form": form})
