import pandas as pd
from django.conf import settings
import os
from .load_excel_data_module import load_course_Int_excel_data,load_free_class_data
from .create_dataframe_module import create_combine_framedata, create_new_dataframe

def Is_True(a,b): #참거짓 판단 함수 a가 작으면 참 bool
    if a<=b:
        return True
    else:
        return False
def Is_graduate():#졸업가능 여부를 색으로 표현해주는 함수 dict
    load_data = load_course_Int_excel_data()
    graduate={ #졸업기준 요건
        'HRD':14,
        'MSC':30,
        '교양':25,
        '자유선택':5,
        '전공':76,
    }
    files = [
    'HRD',
    'MSC',
    '교양',
    '자유선택',
    '전공'
    ]
    graduate_list =[]
    load_list=[]
    return_dict={}
    x=load_free_class_data()
    for k,v in graduate.items():
        graduate_list.append(v)
    for k,v in load_data.items():
        load_list.append(v)
    for a in range(len(graduate_list)-1):
        if files[a]=='자유선택':
            return_dict[files[a]]=Is_True(graduate_list[a],x['total_credits'])
        else:
            return_dict[files[a]]=Is_True(graduate_list[a],load_list[a])
    return return_dict

def Is_change_able(): #알고리즘 기초 데이터를 모으는 함수 void
    create_new_dataframe()
    create_combine_framedata()
    
def Is_over_course_data():#학점이 초과되는 과목들을 반환 list
    tf_list=Is_graduate()
    over_list=[]
    for k,v in tf_list.items():
        if v:
            over_list.append(k)
        else:
            pass
    return over_list
def Is_over_course_class_data(): #학점이 초과되는 과목들과 학점을 반환 dict
    return_data_dict = {}
    over_list = Is_over_course_data()

    for name in over_list:
        file_path = settings.BASE_DIR / 'myapp' / 'data' / f'{name}.xlsx'
        df = pd.read_excel(file_path)

        # 과목 이름만 리스트 형식으로 가져옵니다.
        class_names_list = df['이수현황'].dropna().tolist()  # NaN 값 제거 후 리스트로 변환
        class_ints_list = df['이수학점'].dropna().tolist()

        # 사전에 과목 이름과 이수 학점 리스트를 저장합니다.
        return_data_dict[f'{name}_class_name'] = class_names_list
        return_data_dict[f'{name}_class_int'] = class_ints_list

    return return_data_dict

