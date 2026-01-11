from django.core.management.base import BaseCommand
from vinyl.models import Genre, RecordCondition


class Command(BaseCommand):
    def handle(self, *args, **options):

        genres = ['Рок', 'Поп', 'Джаз', 'Блюз', 'Классика',
                  'Электроника', 'Хип-хоп', 'Фолк', 'Кантри', 'Регги']

        for genre_name in genres:
            Genre.objects.get_or_create(name=genre_name)

        conditions = [
            {
                'grade': 'M',
                'description': 'Идеальное состояние, заводская упаковка'
            },
            {
                'grade': 'M',
                'description': 'Отличное состояние, минимальные следы использования'
            },
            {
                'grade': 'VG',
                'description': 'Очень хорошее, мелкие царапины не влияют на звук'
            },
            {
                'grade': 'VG',
                'description': 'Очень хорошее, потертости на конверте'
            },
            {
                'grade': 'G',
                'description': 'Хорошее, несколько заметных царапин'
            },
            {
                'grade': 'F',
                'description': 'Удовлетворительное, сильные потертости'
            },
            {
                'grade': 'F',
                'description': 'Удовлетворительное, есть вмятины на конверте'
            },
        ]

        for condition in conditions:
            RecordCondition.objects.get_or_create(grade=condition['grade'], description=condition['description'])
