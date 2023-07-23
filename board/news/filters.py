from django.forms import DateTimeInput
from django_filters import FilterSet, DateTimeFilter, ModelChoiceFilter, CharFilter, ModelMultipleChoiceFilter
from .models import *



class PostFilter(FilterSet):
    date_Creation = DateTimeFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        label='Дата написания с',
        widget=DateTimeInput(
            format='%Y-%m-%dT',
            attrs={'type': 'datetime-local'},
        ),
    )

    post_title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Заголовок поста'
    )

    post_Category = ModelMultipleChoiceFilter(
        field_name='postCategory',
        queryset=Category.objects.all(),
        label='Категория поста',
        conjoined=True
    )


# class ResponseFilter(FilterSet):
#     # post_title = CharFilter(
#     #     field_name='title',
#     #     lookup_expr='icontains',
#     #     label='Заголовок поста'
#     # )
#
#     resp_text = CharFilter(
#         field_name='title',
#         lookup_expr='icontains',
#         label='Текст комментария'
#     )
#
#
#     date_Creation = DateTimeFilter(
#         field_name='resp_dateCreation',
#         lookup_expr='gt',
#         label='Дата создания отклика не ранее',
#         widget=DateTimeInput(
#             format='%Y-%m-%dT',
#             attrs={'type': 'datetime-local'},
#         ),
#     )



