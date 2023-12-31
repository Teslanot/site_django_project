from django.shortcuts import render,redirect, get_object_or_404 # для того чтобы отдавать html
from django.urls import reverse #получение ссылки по названию в urls
from .models import Advertisement
# from .forms import AdverisementForm
from .forms import AdvertisementForm
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth.decorators import login_required # если пользователь не авторизован перенаправляем его
from django.urls import reverse_lazy # как reverse но только ленивая функция
from datetime import datetime, timedelta
from django.contrib import messages



# функции-представления
# <!-- {{}}  - это переменная -->
# <!-- {% %}  - это блоки с функционалом -->
# <!-- {% if else while for %}  - это блоки с функционалом -->
User = get_user_model()


def home(request: WSGIRequest):
    title = request.GET.get('query')
    if title: # если пользователь что-то ищет
        data = Advertisement.objects.filter(title__icontains = title) # SELECT * FROM Advertisement WHERE title = title
    else: # если ничего не ищет(просто все обьявления)
        data = Advertisement.objects.all() # беру все записи из БД


    context = {'advertisements' : data, 'title': title} # словарь
    return render(request, 'index.html', context)


def novinki(request:WSGIRequest):
    adv_all= Advertisement.objects.all()
    now = datetime.now() 
    adv_new = now - timedelta(days = 7)
    adv_filter = adv_all.filter(created__gte = adv_new)
    adv_filter = adv_all.filter(created__gte = now)


    title = request.GET.get('query')
    if title: # если пользователь что-то ищет
        adv_filter = Advertisement.objects.filter(created__gte = adv_new, title__icontains = title) # SELECT * FROM Advertisement WHERE title = title
    else: # если ничего не ищет(просто все обьявления)
        adv_filter = adv_all.filter(created__gte = adv_new)
    context = {'advertisements' : adv_filter, 'title': title}
    return render(request, 'novinki.html', context)

def novinki_den(request:WSGIRequest):
    adv_all= Advertisement.objects.all()
    now = datetime.now() 
    adv_filter = adv_all.filter(created__gte = now)
    context = {'advertisements' : adv_filter}
    return render(request, 'novinki_den.html', context)

def top_sellers(request):
    users = User.objects.annotate(
        adv_count = Count('advertisement')# записываю в  adv_count колисчество обьявлений у каждого пользователя
    ).order_by('-adv_count') # сортировка от наибольшего к наименьшему

    context = {"users" : users}
    return render(request, 'top-sellers.html', context)



@login_required
def add_to_favorites(request, pk):
    adv = get_object_or_404(Advertisement, id=pk)
    if request.method == 'POST':
        adv.favorites.add(request.user)
    context = {"adv" : adv}
    return render(request, 'favorite.html', context)
    # if created:
    #     messages.success(request, "Вы добавили объявление в избранное")
    #     # the ad was not in the user's favorites before
    #     # do something, e.g. send a message or redirect to a page
    # else:
    #     messages.error(request, "Это объявление уже в вашем избранном")
    #     # the ad was already in the user's favorites
    #     # do something else, e.g. show an error or redirect to another page

@login_required
def remove_from_favorite(request, pk):
    adv = get_object_or_404(Advertisement, id=pk)
    if request.method == 'POST':
        adv.favorites.clear()
    context = {"adv" : adv}
    return render(request, 'favorite.html', context)


def favorit_list(request):
    adv= Advertisement.objects.all()
    # adv = get_object_or_404(Advertisement, id=pk)
    # adv_filter = adv.filter(adv.favorites == True)
    favorit_list_1 = Advertisement.objects.exclude(favorites= False)

    context = {'favorite_list': favorit_list_1}
    return render(request, 'all-fav.html', context)






def post_adv_detail(request: WSGIRequest, pk):
    # post_adv/<int:pk>/
    # http://127.0.0.1:8000/post_adv/1/
    # pk = 1
    adv = Advertisement.objects.get(id = pk) # ищу запись по id
    context = {"adv" : adv}
    return render(request, 'advertisement.html', context)

# advertisements

# AdvForma
def post_adv(request: WSGIRequest):
    
    print('request.GET',request.GET)
    print('request.POST',request.POST)
    print('request.FILES',request.FILES)
    print('request.user',request.user)

    if request.method == "POST":
        form = AdvertisementForm(request.POST, request.FILES) # передаю данные с запроса на проверку 
        if form.is_valid(): # True/False  проверяю правильность
            # print(request.POST['title'])
            print(form.cleaned_data) # отдает словарь со всеми данными
            adv = Advertisement(**form.cleaned_data)# распаковка словар
            adv.user = request.user # отдельно указал пользователя 
            adv.save()  # сохраняю запись
            return redirect(
                reverse('home') # переадресация на главную страницу 
            )

        else: # если неправильно
            print(form.errors) # вывожу эту ошибку\




    else: # GET или другие
        form = AdvertisementForm() # пустая форма

    context = {'form' : form} # словарь
    return render(request, 'advertisement-post.html', context)


def test(request):
    return render(request, 'test.html')

def test2(request):
    return render(request, 'test2.html')




