import plotly.express as px
import plotly.io as pio
import pandas as pd
from .models import VinylRecord, Genre
from django.db.models import Count, Avg


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
    df = df.sort_values('avg_value')
    df['display_value'] = df['avg_value'].apply(lambda x: f'{int(x)} руб.')

    fig = px.pie(df, values='avg_value', names='genre',
                 color_discrete_sequence=px.colors.sequential.RdBu)

    fig.update_traces(textposition='inside', textinfo='label+text', text=df['display_value'],
                      hovertemplate=None, hoverinfo='skip')

    fig.update_layout(showlegend=True, height=450, hovermode=False)

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
    df = df.sort_values('avg_value')
    df['display_value'] = df['avg_value'].apply(lambda x: f'{int(x)} руб.')

    fig = px.pie(df, values='avg_value', names='format_name', color_discrete_sequence=px.colors.sequential.RdBu)

    fig.update_traces(textposition='inside', textinfo='label+text', text=df['display_value'],
                      hovertemplate=None, hoverinfo='skip')

    fig.update_layout(showlegend=True, height=450, hovermode=False)

    return pio.to_html(fig, full_html=False, include_plotlyjs=True)