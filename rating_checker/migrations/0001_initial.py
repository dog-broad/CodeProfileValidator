# Generated by Django 4.2.11 on 2024-05-11 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Platforms',
            fields=[
                ('platform_id', models.AutoField(primary_key=True, serialize=False)),
                ('platform_name', models.CharField(blank=True, null=True)),
                ('platform_username', models.CharField(blank=True, null=True)),
                ('verification_status', models.CharField(blank=True, null=True)),
                ('platform_data', models.JSONField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'platforms',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SearchTokens',
            fields=[
                ('token_id', models.AutoField(primary_key=True, serialize=False)),
                ('year_of_passing', models.IntegerField(blank=True, null=True)),
                ('urls', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'search_tokens',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('user_id', models.CharField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, null=True)),
                ('email', models.CharField(blank=True, null=True)),
                ('photo_url', models.CharField(blank=True, null=True)),
                ('year_of_passing', models.IntegerField(blank=True, null=True)),
                ('hall_ticket_no', models.CharField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('platforms', models.JSONField(blank=True, null=True)),
            ],
            options={
                'db_table': 'users',
                'managed': False,
            },
        ),
    ]
