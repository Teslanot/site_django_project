from django.urls import path

# импортирую свои представления

from .views import home, test, test2, top_sellers, post_adv,post_adv_detail, novinki, novinki_den,add_to_favorites,remove_from_favorite,favorit_list

#  маршрутизатор приложения 



urlpatterns = [
    path("", home, name = 'home'), # главная страница 
    path("top_sellers/", top_sellers, name='top_sellers'), # топ продавцов 
    path("post_adv/", post_adv, name='post_adv'),
    path("post_adv/<int:pk>", post_adv_detail, name='post_adv_detail'),
    path("test/", test, name = 'test'), 
    path("test2/", test2, name = 'test2'), 
    path("novinki/", novinki, name = 'novinki'), 
    path("novinki_za_den", novinki_den, name='novinki_za_den'), 
    path("favorites/add/<int:pk>", add_to_favorites, name='add_to_favorites'),
    path("favorites/remove/<int:pk>", remove_from_favorite, name='remove_from_favorite'),
    path("favorites", favorit_list, name='favorit_list'),
]       



# для того чтобы отобразить html:
# 1 создать html
# 2 создать функцию представление в views.py
# 3 создать ссылку в urls.py по которой будет вызывать эта функция