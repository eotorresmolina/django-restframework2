from django.urls import path
from apps.e_commerce.api.marvel_api_views import *
from apps.e_commerce.api.index import *

# Importamos las API_VIEWS:
from apps.e_commerce.api.api_views import *

urlpatterns = [
    # User APIs:
    path('user/login/', LoginUserAPIView.as_view()),

    # APIs de Marvel
    path('index/', hello_user),
    path('get_comics/',get_comics),
    path('purchased_item/',purchased_item),
    
    # Comic API View:
    path('comics/get', GetComicAPIView.as_view()),
    path('comics/<comic_id>/get', GetOneComicAPIView.as_view()),
    path('comics/post', PostComicAPIView.as_view()),
    path('comics/get-post', ListCreateComicAPIView.as_view()),
    path('comics/<pk>/update', RetrieveUpdateComicAPIView.as_view()),
    path('comics/<pk>/delete', DestroyComicAPIView.as_view()),

    # TODO: Wish-list API View
    path('wishlist/get', GetWishListAPIView.as_view()),
    path('wishlist/post', PostWishListAPIView.as_view()),
    path('wishlist/get-post', ListCreateWishListAPIView.as_view()),
    path('wishlist/<pk>/update', RetrieveUpdateListWishAPIView.as_view()),
    path('wishlist/<pk>/delete', DestroyWishListAPIView.as_view()),
    path('favs/<username>/get', GetUserFavsAPIView.as_view()),
    path('favs/post', PostUserFavsAPIView.as_view())
]