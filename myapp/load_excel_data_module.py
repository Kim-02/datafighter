
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
    files = [
    'HRD',
    'MSC',
    '교양',
    '자유선택',
    '전공',
    '학부'
    ]
    data ={}
    for input_data in files:
        data.update(load_course_data(input_data))
    for key, value in data.items():#str로 바꿔주는 함수 dict[key] : str
        temp=''
        for a in value:
            if pd.isna(a):
                data[key] = '미이수'
                break
            temp+=f'{a} / '
        else:
            temp =temp[:-3] 
            data[key]=temp
    return data
def load_course_Int_excel_data():
    files = [
    'HRD',
    'MSC',
    '교양',
    '전공',
    '학부'
    ]
    data={}
    out_data={}
    for input_data in files:
        data.update(load_int_data(input_data))
    for key,value in data.items(): #합산해주는 구간
        if pd.isna(value[0]):
            data[key] =0
        else:
            data[key] = sum(value)
    out_data['HRD']=int(data['HRD선택']+data['HRD필수'])
    out_data['MSC']=int(data['MSC선수']+data['MSC필수'])
    out_data['교양']=int(data['교양선택']+data['교양필수'])
    out_data['전공']=int(data['전선']+data['전필']+data['학부선']+data['학부필'])
    return out_data
def load_course_data(course_name):#구분 / 과목명 데이터 가져오는 함수 dict
    file_path = settings.BASE_DIR / 'myapp' / 'data' / f'{course_name}.xlsx'
    df = pd.read_excel(file_path)
    out_list =df[['구분','이수현황']]
    result_dict = out_list.groupby('구분')['이수현황'].apply(list).to_dict()
    # 결과 출력
    return result_dict

def load_int_data(course_name): #이수학점 확인
    
    file_path = settings.BASE_DIR / 'myapp' / 'data' / f'{course_name}.xlsx'
    df = pd.read_excel(file_path)
    out_list =df[['구분','이수학점']]
    result_dict = out_list.groupby('구분')['이수학점'].apply(list).to_dict()
    return result_dict

def load_free_class_data():#자유선택 엑셀 파일의 데이터만 긁어오는 함수 dict
    # 자유선택 엑셀 파일의 경로
    file_path = settings.BASE_DIR / 'myapp' / 'data' / '자유선택.xlsx'
    
    # 엑셀 파일을 읽어옵니다.
    df = pd.read_excel(file_path)
    
    # 과목명과 학점만 선택
    course_list = df[['이수현황', '이수학점']]
    
    # 학점의 총합을 계산합니다.
    total_credits = course_list['이수학점'].sum()
    
    course = df['이수현황'].dropna().tolist()
    out_course =''
    for a in course:
        if pd.isna(a):
            out_course = '미이수'
            break
        out_course+=f'{a} / '
    else:
        out_course =out_course[:-3]
    # 결과를 딕셔너리 형태로 반환
    result = {
        'course_list': out_course,  # 과목명과 학점 데이터를 딕셔너리로 변환
        'total_credits': total_credits
    }
    return result

def load_credit_data(): #그래프를 위한 크레딧 데이터 생성 함수 list
    input_timeline_list=[
        '전공',
        'MSC',
        '교양',
        'HRD',
        '자유선택'
    ]
    return_list=[]
    int_dict = load_course_Int_excel_data()
    free_data = load_free_class_data()
    for i in range(len(input_timeline_list)):
        if i==4:
            return_list.append(int(free_data['total_credits']))
        else:
            return_list.append(int_dict[input_timeline_list[i]])
    return return_list