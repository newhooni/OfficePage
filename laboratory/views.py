from django.shortcuts import render
from django.http import JsonResponse
from .models import DailyNote
from datetime import datetime
from django.db.models import Q # ✅ Q 객체 추가

def index(request):
    return render(request, 'laboratory/index.html')

def get_note(request):
    date_str = request.GET.get('date')
    if not date_str:
        return JsonResponse({'content': ''})

    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()

        # ✅ 핵심 수정: 
        # 1. 선택한 날짜보다 작거나 같고 (date__lte)
        # 2. 내용이 NULL이 아니며 (content__isnull=False)
        # 3. 내용이 빈 문자열이 아닌 (~Q(content='')) 데이터를 찾습니다.
        note = DailyNote.objects.filter(
            date__lte=target_date
        ).exclude(
            Q(content__isnull=True) | Q(content__exact='') | Q(content__exact='<p>&nbsp;</p>')
        ).order_by('-date').first()
        
        return JsonResponse({'content': note.content if note else ''})
    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'content': ''})

def save_note(request):
    if request.method == 'POST':
        date_str = request.POST.get('date')
        content = request.POST.get('content')
        
        # 저장 시에는 NULL 방지를 위해 빈 문자열이라도 넣어서 업데이트
        DailyNote.objects.update_or_create(
            date=date_str,
            defaults={'content': content if content else ''}
        )
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})