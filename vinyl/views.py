import plotly.express as px
import plotly.io as pio
import pandas as pd
from .models import VinylRecord, Genre
from .forms import VinylRecordForm
from django.db.models import Count, Sum, Avg
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


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

    format_stats = records.values('format').annotate(
        total_count=Count('id'),
        avg_value=Avg('estimated_value')
    )

    format_choices = dict(VinylRecord.FORMAT_CHOICES)
    for stat in format_stats:
        stat['format_display'] = format_choices.get(stat['format'], stat['format'])

    chart_data = {
        'genre_count_chart': get_genre_count(request.user),
        'genre_value_chart': get_genre_value(request.user),
        'format_count_chart': get_format_count(request.user),
        'format_value_chart': get_format_value(request.user)
    }

    context = {
        'stats': stats,
        'format_stats': format_stats,
        'chart_data': chart_data,
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
        'title': f'Редактировать {record.artist} - {record.title}'
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


def get_genre_count(user):
    genres = Genre.objects.all()
    data = []
    for genre in genres:
        records = genre.vinylrecord_set.filter(user=user)
        count = records.count()
        if count > 0:
            data.append({
                'genre': genre.name,
                'count': count
            })
    if not data:
        return "<p class='text-muted'>Нет данных по жанрам</p>"

    df = pd.DataFrame(data)
    df['count'] = df['count'].astype(int)

    fig = px.pie(df, values='count', names='genre',
                 color_discrete_sequence=px.colors.sequential.RdBu)

    fig.update_traces(textposition='inside', textinfo='percent+label',
        hovertemplate="<b>%{label}</b><br>" +
                      "Количество: %{value}<br>" +
                      "<extra></extra>")

    fig.update_layout(showlegend=True, height=450)

    return pio.to_html(fig, full_html=False, include_plotlyjs=True)


def get_genre_value(user):
    genres = Genre.objects.all()
    data = []
    for genre in genres:
        user_records = genre.vinylrecord_set.filter(user=user)
        if user_records.exists():
            avg_value = user_records.aggregate(avg=Avg('estimated_value'))['avg'] or 0
            if avg_value > 0:
                data.append({
                    'genre': genre.name,
                    'avg_value': avg_value,
                })
    if not data:
        return "<p class='text-muted'>Нет данных по стоимости жанров</p>"

    df = pd.DataFrame(data)
    fig = px.pie(df, values='avg_value', names='genre',
                 color_discrete_sequence=px.colors.sequential.RdBu)

    fig.update_traces(textposition='inside', textinfo='percent+label',
        hovertemplate="<b>%{label}</b><br>" +
                      "Средняя стоимость: %{value:.0f} ₽<br>" +
                      "<extra></extra>")

    fig.update_layout(showlegend=True, height=450)

    return pio.to_html(fig, full_html=False, include_plotlyjs=True)


def get_format_count(user):
    user_records = VinylRecord.objects.filter(user=user)
    format_stats = user_records.values('format').annotate(count=Count('id'))

    if not format_stats:
        return "<p class='text-muted'>Нет данных по форматам</p>"

    df = pd.DataFrame(list(format_stats))
    format_dict = dict(VinylRecord.FORMAT_CHOICES)
    df['format_name'] = df['format'].map(lambda x: format_dict.get(x, x))

    fig = px.pie(df, values='count', names='format_name', color_discrete_sequence=px.colors.sequential.RdBu)

    fig.update_traces(textposition='inside', textinfo='percent+label',
        hovertemplate="<b>%{label}</b><br>" +
                      "Количество: %{value}<br>" +
                      "<extra></extra>"
    )
    fig.update_layout(showlegend=True, height=450)

    return pio.to_html(fig, full_html=False, include_plotlyjs=True)


def get_format_value(user):
    user_records = VinylRecord.objects.filter(user=user)
    format_values = user_records.values('format').annotate(avg_value=Avg('estimated_value'), count=Count('id'))
    if not format_values:
        return "<p class='text-muted'>Нет данных по стоимости форматов</p>"

    df = pd.DataFrame(list(format_values))
    format_dict = dict(VinylRecord.FORMAT_CHOICES)
    df['format_name'] = df['format'].map(lambda x: format_dict.get(x, x))
    df['avg_value'] = df['avg_value'].astype(float).round(2)

    fig = px.pie(df, values='avg_value', names='format_name', color_discrete_sequence=px.colors.sequential.RdBu)

    fig.update_traces(textposition='inside', textinfo='percent+label',
                      hovertemplate="<b>%{label}</b><br>" +
                                    "Средняя стоимость: %{value:.0f} ₽<br>" +
                                    "<extra></extra>")

    fig.update_layout(showlegend=True, height=450)

    return pio.to_html(fig, full_html=False, include_plotlyjs=True)
