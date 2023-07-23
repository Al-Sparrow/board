from django.urls import path
from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete, PostSearch, ResponsePost, ResponseList, \
   ResponseDelete, response_accept
from django.views.decorators.cache import cache_page


urlpatterns = [
   path('', PostList.as_view(), name='board'),
   path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
   path('search/', PostSearch.as_view()), #поиск постов. need настроить
   path('create/', PostCreate.as_view(), name='post_edit'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'), #зачем эта страница?
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'), #как ограничить только для создателя и админов?
   path('<int:pk>/response/', ResponsePost.as_view(), name='response'), #jnrkbr может видеть тот кто оставил и тот кому пост принадлежит
   path('responses/', ResponseList.as_view(), name='responses'), #кэш можно убрать
   path('responses/<int:pk>/delete/', ResponseDelete.as_view(), name='response_delete'),
   path('responses/<int:pk>/saveresp/', response_accept, name='saveresp')
]

