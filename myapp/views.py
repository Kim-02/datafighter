from django.shortcuts import render, redirect
from django.http import JsonResponse
from .load_excel_data_module import load_course_Int_excel_data,load_course_Str_excel_data,load_excel_data,load_free_class_data
from .analysis_data_module import Is_graduate,Is_over_course_data,Is_over_course_class_data,Is_process_checked_courses,Is_change_able

from .test import get_completion_data

# Create your views here.
def my_view(request):#초기 페이지
    return render(request, 'main_page.html')

def student_UI_view(request):#메인페이지
    std_data = load_excel_data()
    str_data = load_course_Str_excel_data()
    int_data = load_course_Int_excel_data()
    자유선택_data = load_free_class_data()
    graduate_data = Is_graduate()
    using_data={
        'std':std_data,
        's':str_data,
        'i':int_data,
        'flags': graduate_data,#색을 입히는 부분
        '자유선택': 자유선택_data['course_list'],
        '자유선택_학점총계': 자유선택_data['total_credits']
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
        Is_process_checked_courses(checked_courses,dropdown_values)
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

def test_view(request):
    # 데이터 준비
    labels = ['HRD', '교양', 'MSC', '공학필수', '자유선택', '전공', '학부']  # 예시 데이터
    current_credits = [12, 16, 6, 0, 17, 17, 1]  # 현재 이수 학점
    max_credits = [14, 46, 14, 3, 5, 70, 3]  # 최대 학점

    context = {
        'labels': labels,
        'current_credits': current_credits,
        'max_credits': max_credits,
    }

    return render(request,'test_page.html',context)