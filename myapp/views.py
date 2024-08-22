from django.shortcuts import render

# Create your views here.
def my_view(request):
    return render(request, 'main_page.html')

def test_view(request):
    return render(request,'test.html')