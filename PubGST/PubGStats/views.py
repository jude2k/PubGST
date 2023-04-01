# views.py

import io
import datetime
import sys
import json
import datetime
import pandas as pd


from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse
from django.http import JsonResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from chicken_dinner.pubgapi import PUBG
from .db import create_or_add_entries_in_db, close_database_connection, group_by_name_and_date
from .utils import convert_utc_to_cvt


def generate_damage_trend(data):
    # convert the data to a pandas DataFrame
    df = pd.DataFrame(data)
    colors = ['rgb(219, 219, 4)', 'rgb(54, 162, 235)', 'rgb(255, 99, 132)', 'rgb(173, 2, 153)']
    # convert the 'date' column to a pandas datetime object
    df['date'] = pd.to_datetime(df['date'])

    # group the data by player_name and date, and sum the total_damage
    grouped = df.groupby(['player_name', 'date'])['Average damage'].mean().reset_index()

    # pivot the data to have each player_name as a column
    pivoted = grouped.pivot(index='date', columns='player_name', values='Average damage')

    # create a dictionary to store the chart data
    chart_data = {
        'labels': list(pivoted.index.strftime('%Y-%m-%d')),
        'datasets': []
    }

    i = 0
    # add a dataset for each player
    for i, (player_name, player_data) in enumerate(pivoted.items()):
        dataset = {
            'label': player_name,
            'data': list(player_data),
            'fill': False,
            'borderColor': colors[i % len(colors)],
            'lineTension': 0.1
        }
        chart_data['datasets'].append(dataset)

    # render the chart as a JSON string
    chart_json = json.dumps(chart_data)

    return chart_json


def generate_assists_trend(data):
    # convert the data to a pandas DataFrame
    df = pd.DataFrame(data)
    colors = ['rgb(219, 219, 4)', 'rgb(54, 162, 235)', 'rgb(255, 99, 132)', 'rgb(173, 2, 153)']
    # convert the 'date' column to a pandas datetime object
    df['date'] = pd.to_datetime(df['date'])

    # group the data by player_name and date, and calculate the mean assists
    grouped = df.groupby(['player_name', 'date'])['Average assists'].mean().reset_index()

    # pivot the data to have each player_name as a column
    pivoted = grouped.pivot(index='date', columns='player_name', values='Average assists')

    # create a dictionary to store the chart data
    chart_data = {
        'labels': list(pivoted.index.strftime('%Y-%m-%d')),
        'datasets': []
    }
    i = 0
    # add a dataset for each player
    for i, (player_name, player_data) in enumerate(pivoted.items()):
        dataset = {
            'label': player_name,
            'data': list(player_data),
            'fill': False,
            'borderColor': colors[i % len(colors)],
            'lineTension': 0.1
        }
        chart_data['datasets'].append(dataset)

    # render the chart as a JSON string
    chart_json = json.dumps(chart_data)

    return chart_json

def generate_kills_trend(data):
    # convert the data to a pandas DataFrame
    df = pd.DataFrame(data)
    colors = ['rgb(219, 219, 4)', 'rgb(54, 162, 235)', 'rgb(255, 99, 132)', 'rgb(173, 2, 153)']
    # convert the 'date' column to a pandas datetime object
    df['date'] = pd.to_datetime(df['date'])

    # group the data by player_name and date, and sum the kills
    grouped = df.groupby(['player_name', 'date'])['Average kills'].mean().reset_index()

    # pivot the data to have each player_name as a column
    pivoted = grouped.pivot(index='date', columns='player_name', values='Average kills')

    # create a dictionary to store the chart data
    chart_data = {
        'labels': list(pivoted.index.strftime('%Y-%m-%d')),
        'datasets': []
    }
    i = 0
    # add a dataset for each player
    for i, (player_name, player_data) in enumerate(pivoted.items()):
        dataset = {
            'label': player_name,
            'data': list(player_data),
            'fill': False,
            'borderColor': colors[i % len(colors)],
            'lineTension': 0.1
        }
        chart_data['datasets'].append(dataset)

    # render the chart as a JSON string
    chart_json = json.dumps(chart_data)

    return chart_json 
    

def generate_dbnos_trend(data):
    # convert the data to a pandas DataFrame
    df = pd.DataFrame(data)
    colors = ['rgb(219, 219, 4)', 'rgb(54, 162, 235)', 'rgb(255, 99, 132)', 'rgb(173, 2, 153)']
    # convert the 'date' column to a pandas datetime object
    df['date'] = pd.to_datetime(df['date'])

    # group the data by player_name and date, and calculate the average_dbnos
    grouped = df.groupby(['player_name', 'date'])['Average dbnos'].mean().reset_index()

    # pivot the data to have each player_name as a column
    pivoted = grouped.pivot(index='date', columns='player_name', values='Average dbnos')
    # create a list of colors to use for each player
    
    # create a dictionary to store the chart data
    chart_data = {
        'labels': list(pivoted.index.strftime('%Y-%m-%d')),
        'datasets': []
    }
    i = 0
    # add a dataset for each player
    for i, (player_name, player_data) in enumerate(pivoted.items()):
        dataset = {
            'label': player_name,
            'data': list(player_data),
            'fill': False,
            'borderColor': colors[i % len(colors)],
            'lineTension': 0.1
        }
        chart_data['datasets'].append(dataset)

    # render the chart as a JSON string
    chart_json = json.dumps(chart_data)

    return chart_json


def run_script(data):
    api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJmNTNiNWI1MC03ZjA2LTAxM2ItNWIwYS00MzEzOWVkOWU4NmYiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjc0NjY5MTQ4LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6ImJvZ2RhbmFwcCJ9.saoty3AwtsqfJFVxvssaU1oUJS8jNLC22fCOf7exC5o"
    pubg = PUBG(api_key=api_key, shard="steam")

    # Creates a Players instance (iterable of Player instances)
    players = pubg.players_from_names(data)

    shared_matches = players.shared_matches()


    # Get the current date and time in UTC
    current_time = datetime.datetime.utcnow()

    # Calculate the date and time 24 hours ago
    delta = datetime.timedelta(hours=200)
    start_time = current_time - delta

    # Format the start and end times as ISO 8601 strings
    start_time_str = start_time.isoformat() + "Z"
    end_time_str = current_time.isoformat() + "Z"


    for i, player in enumerate(players):
        globals()[f"player{i+1}"] = player

    matches_count = 0

    for match in shared_matches:

        stats = []

        current_match = pubg.match(match)
        if start_time_str <= current_match.created_at <= end_time_str:
            if current_match.game_mode == 'squad-fpp':
                rosters = current_match.rosters
                for roster in rosters:
                    if player1.name in roster.player_names:
                        found_roster = roster
                        matches_count += 1
                # Participant from a roster
                roster_participants = found_roster.participants
                match_id = current_match.match_id
                created_at = current_match.created_at

                player_vars = {}
                for i, player in enumerate(players):
                    player_vars[player.name] = f"player{i + 1}"

                stats = []
                player_stats = {}
                for participant in roster_participants:
                    for player_name, player_var in player_vars.items():
                        if player_name in participant.name:
                            player_stats[player_name] = {
                                'Kills': participant.stats.get('kills'),
                                'Assists': participant.stats.get('assists'),
                                'Dbnos': participant.stats.get('dbnos'),
                                'Total Damage': participant.stats.get('damage_dealt')
                            }
                stats.append(player_stats)


                create_or_add_entries_in_db(stats[0], match_id, convert_utc_to_cvt(created_at))

    group = group_by_name_and_date(data)

    close_database_connection()

    return group

class PlayerForm(forms.Form):
    player1 = forms.CharField(max_length=50)
    player2 = forms.CharField(max_length=50)
    player3 = forms.CharField(max_length=50)
    player4 = forms.CharField(max_length=50)


def addplayers(request):
    if request.method == 'POST':
        # get the player names from the form data
        player1 = request.POST.get('player1')
        player2 = request.POST.get('player2')
        player3 = request.POST.get('player3')
        player4 = request.POST.get('player4')
        players = [player for player in [player1, player2, player3, player4] if player]

        # run the data analysis script and pass in the players list
        stats = run_script(players)
        response = run_script_view(request, stats)
        return response

    else:
        return render(request, 'addplayers.html')




def run_script_view(request, data):
    
    # get the images from the data and pass them to the template
    damage_trend_data = generate_damage_trend(data)
    
    kills_trend_data = generate_kills_trend(data)
    assists_trend_data = generate_assists_trend(data)
    dbnos_trend_data = generate_dbnos_trend(data)

    return render(request, 'results.html', {
        'damage_trend_data': damage_trend_data,
        'kills_trend_data': kills_trend_data,
        'assists_trend_data': assists_trend_data,
        'dbnos_trend_data': dbnos_trend_data,
})

