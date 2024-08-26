from django.shortcuts import render
import pandas as pd
from django.conf import settings

def create_new_dataframe():#2021대학요람 기준 데이터베이스를 만드는 함수
    file_path = settings.BASE_DIR / 'myapp' / 'data' / '2021data.xlsx'
    df = pd.read_excel(file_path)
    unique_courses_list = []
    seen_courses = set()
    for index, row in df.iterrows():
        course_key = (row['과목코드'], row['교과목명'])  # 중복 검사 기준: 과목 코드와 교과목명
        if course_key not in seen_courses:
            seen_courses.add(course_key)  # 세트에 추가하여 중복 방지
            unique_courses_list.append(row)  # 중복되지 않은 행만 리스트에 추가
    unique_courses_df = pd.DataFrame(unique_courses_list)
    output_df = unique_courses_df[['과목코드', '교과목명', '학점']]
    output_file_path = settings.BASE_DIR / 'myapp' / 'data' / 'drop_dup.xlsx'
    output_df.to_excel(output_file_path, index=False)