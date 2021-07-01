from django.urls import path

from .views import create_result, edit_results, all_results_view,all_results_view_class,add_score

urlpatterns = [
  path('create/', create_result, name='create-result'),
  path('edit-results/', edit_results, name='edit-results'),
  path('view/all', all_results_view, name='view-results'),
  path('view/all_class',all_results_view_class,name='results-class'),
  path('edit-class_results/',add_score,name='grade-override')
]
