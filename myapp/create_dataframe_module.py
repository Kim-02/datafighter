from django.shortcuts import render
import pandas as pd
from django.conf import settings
import os

def create_new_dataframe():
    # 1학기 데이터 경로
    file_path_1st = settings.BASE_DIR / 'myapp' / 'data' / '2021data_1.xlsx'
    
    # 2학기 데이터 경로
    file_path_2nd = settings.BASE_DIR / 'myapp' / 'data' / '2021data_2.xlsx'
    
    # 1학기 데이터 읽기
    df_1st = pd.read_excel(file_path_1st)
    
    # 2학기 데이터 읽기
    df_2nd = pd.read_excel(file_path_2nd)

    # 중복 제거 로직 (1학기)
    unique_courses_list_1st = []
    seen_courses = set()
    for index, row in df_1st.iterrows():
        course_key = (row['과목코드'], row['교과목명'])
        if course_key not in seen_courses:
            seen_courses.add(course_key)
            unique_courses_list_1st.append(row)
    
    unique_courses_df_1st = pd.DataFrame(unique_courses_list_1st)

    # 동일한 중복 제거 로직 (2학기)
    unique_courses_list_2nd = []
    for index, row in df_2nd.iterrows():
        course_key = (row['과목코드'], row['교과목명'])
        if course_key not in seen_courses:
            seen_courses.add(course_key)
            unique_courses_list_2nd.append(row)
    
    unique_courses_df_2nd = pd.DataFrame(unique_courses_list_2nd)

    # 두 학기 데이터를 병합 (concat으로 위아래로 이어붙임)
    merged_df = pd.concat([unique_courses_df_1st, unique_courses_df_2nd])

    # 필요 컬럼만 선택
    output_df = merged_df[['대표이수구분','과목코드', '교과목명', '학점']]
    
    # 중복된 파일 저장 경로 설정
    output_file_path = settings.BASE_DIR / 'myapp' / 'data' / 'drop_dup.xlsx'
    
    # 결과를 엑셀로 저장
    output_df.to_excel(output_file_path, index=False)

def create_combine_framedata():#이수구분별로 한개의 파일로 합치는 함수
    files = [
    'HRD.xlsx',
    'MSC.xlsx',
    '공학필.xlsx',
    '교양.xlsx',
    '자유선택.xlsx',
    '전공.xlsx',
    '학부.xlsx'
    ]
    data_frames = []
    for file in files:
        division = os.path.splitext(file)[0]
        # 엑셀 파일 읽기
        file_path = settings.BASE_DIR / 'myapp' / 'data' / file
        df = pd.read_excel(file_path)
        
        # '구분' 열 추가
        df['구분'] = division
        
        # 데이터프레임 리스트에 추가
        data_frames.append(df)
    combined_df = pd.concat(data_frames, ignore_index=True)

    # 원하는 파일명으로 저장
    output_file_path = settings.BASE_DIR / 'myapp' / 'data' / 'combine_data.xlsx'
    combined_df.to_excel(output_file_path, index=False)