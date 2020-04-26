from django.shortcuts import render


def index(request):
    if 'selectedLanguage' not in request.COOKIES:
        print('쿠키 없음')
    else:
        cookie = request.COOKIES['selectedLanguage']
        
        print(f'cookie: {cookie}')

    return render(request, 'cookietest/index.html')
