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
    graduate={
        'HRD':14,
        'MSC':9,
        '공학필':3,
        '교양':46,
        '자유선택':5,
        '전공':70,
        '학부':3
    }
    files = [
    'HRD',
    'MSC',
    '공학필',
    '교양',
    '자유선택',
    '전공',
    '학부'
    ]
    graduate_list =[]
    load_list=[]
    return_dict={}
    x=load_free_class_data()
    for k,v in graduate.items():
        graduate_list.append(v)
    for k,v in load_data.items():
        load_list.append(v)
    for a in range(len(graduate_list)):
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

def Is_get_course_row(course, selected_course):
    """
    주어진 과목(course) 파일에서 선택된 과목명(selected_course)을 찾아 해당 행을 반환하고,
    그 행을 원본 파일에서 삭제한 후 업데이트합니다.
    """
    file_path = os.path.join(settings.BASE_DIR, 'myapp', 'data', f'{course}.xlsx')
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        # 선택된 과목명에 해당하는 행을 찾습니다.
        row_to_move = df[df['이수현황'] == selected_course]
        if not row_to_move.empty:
            # 해당 행을 제거한 데이터프레임으로 업데이트
            df = df[df['이수현황'] != selected_course]
            df.to_excel(file_path, index=False)  # 원본 파일 업데이트
            return row_to_move
    return None
def Is_append_row_to_target(row, target_file_name='자유선택.xlsx'):
    """
    주어진 행(row)을 자유선택.xlsx 파일의 가장 아래로 추가합니다.
    """
    target_file_path = os.path.join(settings.BASE_DIR, 'myapp', 'data', target_file_name)
    if os.path.exists(target_file_path):
        target_df = pd.read_excel(target_file_path)
        # 해당 행을 자유선택 파일의 가장 아래로 추가합니다.
        target_df = pd.concat([target_df, row], ignore_index=True)
        # 자유선택 파일을 다시 저장합니다.
        target_df.to_excel(target_file_path, index=False)
    else:
        print(f"Target file {target_file_name} not found.")
def Is_process_checked_courses(checked_courses, dropdown_values): #초과학점 선택된 것을 자유학점으로 넘기는 함수 void
    """
    체크된 과목들에 대해 자유선택.xlsx 파일로 행을 이동시키고 원본 파일에서 제거하는 전체 과정을 처리합니다.
    """
    for course in checked_courses:
        selected_course = dropdown_values.get(course)
        row_to_move = Is_get_course_row(course, selected_course)
        if row_to_move is not None:
            Is_append_row_to_target(row_to_move)