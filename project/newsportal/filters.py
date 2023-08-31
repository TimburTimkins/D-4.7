from django_filters import FilterSet, DateTimeFilter, ModelChoiceFilter
from django.forms import DateTimeInput
from .models import News


class NewsFilter(FilterSet):
    added_after = DateTimeFilter(
        field_name='date_on',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%d',
            attrs={'type': 'datetime-local'},
        ),
    )


    class Meta:
        model = News
        fields = {
            'name': ['icontains'],
            'type': ['exact'],
            # 'category': ['icontains'],
        }