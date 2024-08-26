from django.shortcuts import render
import pandas as pd
from django.conf import settings
from .load_excel_data_module import load_course_Int_excel_data,load_course_Str_excel_data,load_excel_data
from .create_dataframe_module import create_new_dataframe
#def

# Create your views here.
def my_view(request):
    return render(request, 'main_page.html')

def student_UI_view(request):
    std_data = load_excel_data()
    str_data = load_course_Str_excel_data()
    int_data = load_course_Int_excel_data()
    using_data={
        'std':std_data,
        's':str_data,
        'i':int_data
    }
    create_new_dataframe()
    return render(request,'student_UI.html',using_data)
