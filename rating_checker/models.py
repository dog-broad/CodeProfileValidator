from django.db import models


class PlatformData(models.Model):
    platform_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    platform_name = models.CharField()
    platform_username = models.CharField()
    verification_status = models.CharField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'platform_data'
        unique_together = (('platform_name', 'platform_username'),)


class SearchTokens(models.Model):
    token_id = models.AutoField(primary_key=True)
    year_of_passing = models.IntegerField(blank=True, null=True)
    urls = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'search_tokens'


class Users(models.Model):
    user_id = models.CharField(primary_key=True)
    name = models.CharField(blank=True, null=True)
    email = models.CharField(blank=True, null=True)
    photo_url = models.CharField(blank=True, null=True)
    year_of_passing = models.IntegerField(blank=True, null=True)
    hall_ticket_no = models.CharField(unique=True, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    platforms = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'

