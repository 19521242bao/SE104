from collections import Counter

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.views.generic import ListView

from apps.corecode.models import AcademicSession, AcademicTerm,StudentClass
from apps.students.models import Student

from .models import Result
from .forms import CreateResults, EditResults

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
        current_class=form.cleaned_data['current_class']
        results = []
        print(subjects)
        print(students)
        print(current_class)
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
def all_results_view(request):
  results = Result.objects.filter(
      session=request.current_session, term=request.current_term)
  bulk = {}

  # for result in (results):
  #   print(result.current_class)
  subject_class = dict()
  score_class = dict()
  # for result in results:
  #   if result.current_class not in subject_class.keys():
  #     score_class[result.current_class] = (result.test_score + result.exam_score)
  #     subject_class[result.current_class]=1
  #   else:
  #     score_class[result.current_class] += (result.test_score + result.exam_score)
  #     subject_class[result.current_class] += 1
  # print(score_class.keys())
  # print(subject_class)
  # for result in results:
  #   test_total = 0
  #   exam_total = 0
  #   subjects = []
  #   for subject in results:
  #     print(subject.current_class)
  #     if subject.student == result.student:
  #       subjects.append(subject)
  #       subject.test_score = float(subject.test_score)
  #       subject.exam_score = float(subject.exam_score)
  #       test_total = (test_total + subject.test_score)
  #       exam_total = (exam_total + subject.exam_score)
  #   test_total = test_total / len(subjects)
  #   exam_total = exam_total / len(subjects)
  #   bulk[result.student.id] = {
  #     "student": result.student,
  #     "subjects": subjects,
  #     "test_total": test_total,
  #     "exam_total": exam_total,
  #     "total_total": round((test_total + exam_total) / 2, 2)
  #   }
  classlist=[]
  for result in results:
<<<<<<< Updated upstream
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
      "total_total": round((test_total + exam_total)/2, 2)
    }
=======
    test_class = 0
    exam_class = 0
    total_average=0
    total_total=0
    grade=dict()
    class_member= []
    countA=0
    countD=0
    countC=0
    countB=0
    if result.current_class not in classlist:
      classlist.append(result.current_class)
      for student in results:
        if student.current_class == result.current_class:
          class_member.append(student)
          exam_class+=student.exam_score
          test_class+=student.test_score
          total_total=student.exam_score+student.test_score
          score_rank=score_grade(total_total)
          if score_rank=='A':
            countA+=1
          if score_rank=='B':
            countB+=1
          if score_rank=='C':
            countC+=1
          if score_rank=='D':
            countD+=1
      exam_average=exam_class/len(class_member)
      test_average=test_class/(len(class_member))
      print(class_member)
      print(len(class_member))
      bulk[result.current_class.id] = {
              "name_class":result.current_class,
              "students": class_member,
              "test_average": test_average,
              "exam_average": exam_average,
              "total_average": round((test_average + exam_average) / 2, 3),
              "rankA":countA,
              "rankB": countB,
              "rankC": countC,
              "rankD": countD

      }


>>>>>>> Stashed changes

  context = {
      "results": bulk
  }
  return render(request, 'result/all_results_class.html', context)
# def all_results_view_class(request):
#   results = Result.objects.filter(
#       session=request.current_session, term=request.current_term)
#   bulk = {}
#   print("test output")
#   print(results)
#   subject_class=dict()
#   score_class=dict()
#   for result in results:
#     if result.current_class not in subject_class.keys():
#       score_class[result.current_class]=(result.test_score+result.exam_score)
#       subject_class[result.current_class]=1
#     else:
#       score_class[result.current_class]+=(result.test_score+result.exam_score)
#       subject_class[result.current_class]+=1
#     # for student in results:
#     #     subjects.append(subject)
#     # subjects=dict(Counter(subjects))
#     # total_score=(test_total + exam_total)
#     # bulk[result.student.id] = {
#     #   "student": result.student,
#     #   "subjects": subjects,
#     #   "test_total": round(test_total/count_subject,2),
#     #   "exam_total": round(exam_total/count_subject,2),
#     #   "total_total": round(total_score/count_subject,2),
#     # }
#
#
#   context = {
#       "results": subjects,
#
#   }
#   return render(request, 'result/all_results_class.html', subjects)
def score_grade(score):
  if score <= 10 and score >= 8:
    return 'A'
  elif score < 8 and score >= 6.5:
    return 'B'
  elif score < 6.5 and score >= 5:
    return 'C'
  elif score >= 0 and score < 5:
    return 'D'
  else:
    return "Invalid Score"