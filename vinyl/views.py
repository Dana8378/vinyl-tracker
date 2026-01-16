from .models import VinylRecord
from .forms import VinylRecordForm
from django.db.models import Count, Sum, Avg
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .charts import get_format_count, get_format_value, get_genre_value, get_genre_count


def home(request):
    context = {
        'title': 'Трекер виниловых пластинок',
        'message': 'Добро пожаловать! Начните добавлять свою коллекцию.'
    }

    return render(request, 'vinyl/home.html', context)


@login_required
def vinyl_list(request):
    records = VinylRecord.objects.filter(user=request.user)
    context = {
        'records': records,
        'title': 'Моя коллекция',
        'total_count': records.count()
    }

    return render(request, 'vinyl/list.html', context)


@login_required
def statistics(request):
    records = VinylRecord.objects.filter(user=request.user)
    stats = records.aggregate(
        total_count=Count('id'),
        total_value=Sum('estimated_value'),
        avg_value=Avg('estimated_value')
    )

    chart_data = {
        'genre_count_chart': get_genre_count(request.user),
        'genre_value_chart': get_genre_value(request.user),
        'format_count_chart': get_format_count(request.user),
        'format_value_chart': get_format_value(request.user)
    }

    top_5_expensive_records = records.order_by('-estimated_value')[:5]

    context = {
        'stats': stats,
        'chart_data': chart_data,
        'top_5': top_5_expensive_records,
        'title': 'Статистика коллекции'
    }

    return render(request, 'vinyl/statistic.html', context)


@login_required
def add_record(request):
    if request.method == 'POST':
        form = VinylRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user
            record.save()
        return redirect('vinyl:vinyl_list')
    else:
        form = VinylRecordForm()

    return render(request, 'vinyl/add_form.html', {
        'form': form,
        'title': 'Добавить пластинку'
    })


@login_required
def edit_record(request, record_id):
    record = get_object_or_404(VinylRecord, id=record_id, user=request.user)
    if request.method == 'POST':
        form = VinylRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('vinyl:vinyl_list')
    else:
        form = VinylRecordForm(instance=record)

    return render(request, 'vinyl/edit_form.html', {
        'form': form,
        'record': record,
        'title': f'Редактировать'
    })


@login_required
def delete_record(request, record_id):
    record = get_object_or_404(VinylRecord, id=record_id, user=request.user)
    if request.method == 'POST':
        record.delete()
        return redirect('vinyl:vinyl_list')

    return render(request, 'vinyl/delete_confirm.html', {
        'record': record,
        'title': 'Удалить пластинку'
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('vinyl:home')
    else:
        form = UserCreationForm()

    return render(request, 'vinyl/register.html', {'form': form})
