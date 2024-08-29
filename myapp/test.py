def get_completion_data():
    """
    학점 데이터를 가져오는 함수입니다. 실제 데이터 처리 로직은 여기에서 수행됩니다.
    """
    # 임시 데이터 예시 (엑셀에서 읽어와도 동일한 포맷으로 준비하면 됩니다)
    completion_data = {
        'HRD': {'current': 12, 'max': 14},
        '교양': {'current': 16, 'max': 46},
        'MSC': {'current': 6, 'max': 14},
        '공학필수': {'current': 0, 'max': 3},
        '자유선택': {'current': 17, 'max': 5},
        '전공': {'current': 17, 'max': 70},
        '학부': {'current': 1, 'max': 3}
    }
    return completion_data