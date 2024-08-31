from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .load_excel_data_module import load_course_Int_excel_data,load_course_Str_excel_data,load_excel_data,load_free_class_data,load_credit_data,load_course_data
from .analysis_data_module import Is_graduate,Is_over_course_data,Is_over_course_class_data,Is_change_able
from .update_module import update_userdata,update_checked_courses
from .test import *
import pandas as pd
from django.conf import settings

# Create your views here.
def my_view(request):#초기 페이지
    return render(request, 'main_page.html')

def student_UI_view(request):#메인페이지
    std_data = load_excel_data()
    str_data = load_course_Str_excel_data()
    int_data = load_course_Int_excel_data()
    자유선택_data = load_free_class_data()
    graduate_data = Is_graduate()
    labels = [
        '전공',
        'MSC',
        '교양',
        'HRD',
        '자유선택'
    ]  #순서
    current_credits = load_credit_data()  # 현재 이수 학점
    max_credits = [76, 30, 25, 14, 5]  # 최대 학점
    using_data={
        'std':std_data,
        's':str_data,
        'i':int_data,
        'flags': graduate_data,#색을 입히는 부분
        '자유선택': 자유선택_data['course_list'],
        '자유선택_학점총계': 자유선택_data['total_credits'],
        'labels': labels,
        'current_credits': current_credits,
        'max_credits': max_credits,
    }
    return render(request,'student_UI.html',using_data)

def run_function(request):#test버튼 / 현기능 : 파일 종합 함수
    message="요청을 성공적으로 처리했습니다!"
    Is_change_able()
    return JsonResponse({"message": f"{message}"},safe=False)

def refuse_page_view(request): #자유학점 전환 모뎀 호출함수
    # 기존 함수 호출
    change_class = Is_over_course_data()
    class_data = Is_over_course_class_data()  # {'MSC_class_name': ['공학수학2', ...], 'MSC_class_int': [3, ...]}

    if request.method == "POST":
        # 체크된 과목들 가져오기
        checked_courses = request.POST.getlist('course_checkbox')
        
        # 각 체크된 과목의 드롭다운 선택값 가져오기
        dropdown_values = {}
        for course in checked_courses:
            dropdown_key = f'course_select_{course}'
            dropdown_values[course] = request.POST.get(dropdown_key)
        
        # 데이터 확인 후, 필요한 로직 수행
        result = {
            'checked_courses': checked_courses,
            'dropdown_values': dropdown_values
        }
        # print(result)  # 콘솔에 결과 출력
        update_checked_courses(checked_courses,dropdown_values)
        # 로직을 수행한 후 student_UI_view로 리디렉션
        return redirect('student_UI_view')
    
    else:
        # GET 요청 처리
        processed_data = []

        # 데이터 가공: change_class의 각 항목에 대해 필요한 데이터를 추출
        for item in change_class:
            class_name_key = f"{item}_class_name"
            class_int_key = f"{item}_class_int"
            if class_name_key in class_data and class_int_key in class_data:
                names = class_data[class_name_key]
                ints = class_data[class_int_key]
                combined = zip(names, ints)  # 과목명과 학점을 하나로 묶음
                processed_data.append({'item': item, 'courses': list(combined)})

        # 템플릿에 사용할 데이터를 using_data에 추가
        using_data = {
            'change': change_class,
            'processed_data': processed_data
        }

        return render(request, 'refuse_page.html', using_data)

def change_info_view(request):#개인정보 변경 모뎀 호출함수
    if request.method == "POST":
        # 사용자가 입력한 데이터를 받아 리스트에 저장
        user_data = [
            request.POST.get('name'),
            int(request.POST.get('std_ID')),
            request.POST.get('department'),
            request.POST.get('major'),
            request.POST.get('grade'),  # 드롭다운에서 가져오는 학년 데이터
            request.POST.get('in_School'),  # 드롭다운에서 가져오는 학적상태 데이터
            int(request.POST.get('enter_year')),  # 드롭다운에서 가져오는 교육과정 데이터
            request.POST.get('course'),  # 드롭다운에서 가져오는 학생구분 데이터
        ]

        # 사용자에게 변경 완료를 알림
        update_userdata(user_data)

        # 변경 후 사용자 인터페이스 페이지로 리디렉션
        return redirect('student_UI_view')
    else:#get 요청 처리
        return render(request, 'change_info_page.html')

def recomend_page_view(request):
    # 엑셀 파일 경로 설정
    file_path = settings.BASE_DIR / 'myapp' / 'data' / 'main_data_2021.xlsx'
    
    # 엑셀 파일을 읽고 필터링
    df = pd.read_excel(file_path)
    filtered_df = df[df['대표이수구분'] == 'MSC선수']
    
    # 필요한 컬럼만 추출
    msc_courses = filtered_df[['과목코드', '교과목명']].values.tolist()
    
    if request.method == "POST":
        # 선택된 과목들을 처리
        selected_courses = request.POST.getlist('selected_courses')
        print("선택된 과목들:", selected_courses)
        
        # 이후 student_UI_view로 리디렉션
        return redirect('student_UI_view')
    
    # 필터링된 데이터를 컨텍스트로 전달
    context = {
        'msc_courses': msc_courses,
    }
    
    return render(request, 'recomend_page.html', context)

def change_simulation_view(request):
    # 파일 경로 설정
    main_data_path = settings.BASE_DIR / 'myapp' / 'data' / 'main_data_2021.xlsx'
    user_data_path = settings.BASE_DIR / 'myapp' / 'data' / 'user_combine_data.xlsx'

    # 엑셀 파일 읽기
    main_data = pd.read_excel(main_data_path)
    user_data = pd.read_excel(user_data_path)

    # 필요한 데이터 컬럼 추출
    user_courses = user_data['과목코드'].tolist()
    graph_data = []

    for index, row in main_data.iterrows():
        code = row['과목코드']
        replacement_2022 = row['대체교과목코드_2022']
        replacement_2023 = row['대체교과목코드_2023']
        replacement_2024 = row['대체교과목코드_2024']

        # 노드 색상 정보 추가 (서버에서 판단)
        color_2022 = '#FFEBEE' if replacement_2022 in user_courses else '#D3D3D3'
        color_2023 = '#FFEBEE' if replacement_2023 in user_courses else '#D3D3D3'
        color_2024 = '#FFEBEE' if replacement_2024 in user_courses else '#D3D3D3'

        if replacement_2022 in user_courses or replacement_2023 in user_courses or replacement_2024 in user_courses:
            graph_data.append((code, replacement_2022, replacement_2023, replacement_2024, color_2022, color_2023, color_2024))

    context = {
        'graph_data': graph_data,
        'user_courses': user_courses,
    }
    return render(request, 'change_simulation_page.html', context)




def test_view(request):#테스트용 더미 데이터
    # # 데이터 준비
    # labels = ['HRD', '교양', 'MSC', '공학필수', '자유선택', '전공', '학부']  # 예시 데이터
    # current_credits = [12, 16, 6, 0, 17, 17, 1]  # 현재 이수 학점
    # max_credits = [14, 46, 14, 3, 5, 70, 3]  # 최대 학점

    # context = {
    #     'labels': labels,
    #     'current_credits': current_credits,
    #     'max_credits': max_credits,
    # }

    return render(request,'test_page.html')