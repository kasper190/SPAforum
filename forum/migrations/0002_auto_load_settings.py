# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def load_settings(apps, schema_editor):
	ForumSettings = apps.get_model("forum", "ForumSettings")
	db_alias = schema_editor.connection.alias
	ForumSettings.objects.using(db_alias).bulk_create([
		ForumSettings(forum_name="My Forum"),
	])


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
    	migrations.RunPython(load_settings),
    ]
