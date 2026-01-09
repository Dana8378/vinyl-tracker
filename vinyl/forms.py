from django import forms
from .models import VinylRecord, Genre, RecordCondition


class VinylRecordForm(forms.ModelForm):

    class Meta:
        model = VinylRecord
        fields = [
            'title', 'artist', 'year', 'format',
            'genre', 'condition', 'estimated_value',
            'purchase_price'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['genre'].queryset = Genre.objects.all()
        self.fields['condition'].queryset = RecordCondition.objects.all()