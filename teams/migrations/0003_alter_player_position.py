# Generated by Django 4.2.6 on 2023-10-10 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0002_remove_player_team_team_player_teams'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='position',
            field=models.CharField(choices=[('WicketKeeper', 'WicketKeeper'), ('Batsman', 'Batsman'), ('Bowler', 'Bowler'), ('AllRounder', 'AllRounder')], max_length=100),
        ),
    ]
