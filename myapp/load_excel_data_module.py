from django.shortcuts import render
import pandas as pd
from django.conf import settings

def load_excel_data():
    # 엑셀 파일을 읽어옴 (엑셀 파일 경로를 지정)
    file_path = settings.BASE_DIR / 'myapp' / 'data' / 'userdata.xlsx'
    df = pd.read_excel(file_path)
    # 데이터프레임에서 필요한 데이터 추출 (첫 번째 행의 데이터)
    data = {
        'name': df.iloc[0]['이름'],
        'std_ID': df.iloc[0]['학번'],
        'department': df.iloc[0]['학과'],
        'major': df.iloc[0]['전공'],
        'grade': df.iloc[0]['학년'],
        'in_School': df.iloc[0]['학적상태'],
        'enter_year':df.iloc[0]['교육과정'],
        'course':df.iloc[0]['학생구분']
    }
    return data
def load_course_Str_excel_data():
    data ={
        'S_HRD':load_str_data('HRD'),
        'S_major':load_str_data('전공필수'),
        'S_contect':load_str_data('의사소통'),
        'S_global':load_str_data('글로벌'),
        'S_history':load_str_data('역사와철학'),
        'S_art':load_str_data('예술과문학'),
        'S_network':load_str_data('사회와심리'),
        'S_mix':load_str_data('융합'),
        'S_nawori':load_str_data('나우르인성'),
        'S_study':load_str_data('학습역량'),
        'S_HRD_major':load_str_data('전공HRD융합'),
        'S_MSC':load_str_data('MSC'),
        'S_free':load_str_data('자유선택')
    }
    return data
def load_course_Int_excel_data():
    data ={
        'I_HRD':load_int_data('HRD'),
        'I_major':load_int_data('전공필수'),
        'I_contect':load_int_data('의사소통'),
        'I_global':load_int_data('글로벌'),
        'I_history':load_int_data('역사와철학'),
        'I_art':load_int_data('예술과문학'),
        'I_network':load_int_data('사회와심리'),
        'I_mix':load_int_data('융합'),
        'I_nawori':load_int_data('나우르인성'),
        'I_study':load_int_data('학습역량'),
        'I_HRD_major':load_int_data('전공HRD융합'),
        'I_MSC':load_int_data('MSC'),
        'I_free':load_int_data('자유선택')
    }
    return data
def load_str_data(course_name): #이수과목 확인
    file_path = settings.BASE_DIR / 'myapp' / 'data' / f'{course_name}.xlsx'
    df = pd.read_excel(file_path)
    name_list = df['이수현황'].tolist()
    if len(name_list)==0: #만약 리스트가 비어있다면 실행한다.
        names = '미이수'
    else:
        names=''
        for name in name_list:
            names+=name+' / '
    return names
def load_int_data(course_name): #이수학점 확인
    
    file_path = settings.BASE_DIR / 'myapp' / 'data' / f'{course_name}.xlsx'
    df = pd.read_excel(file_path)
    num_list = df['이수학점'].tolist()
    if df.isnull().values.any(): #결측값을 확인하는 구문 만약 nan이 있으면 True를 반환한다.
        return_num = 0
    else:
        return_num=sum(num_list)
    return return_num