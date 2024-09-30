# Generated by Django 4.2 on 2024-09-30 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transitionentry',
            options={'ordering': ['transition'], 'verbose_name': 'Transition Entry', 'verbose_name_plural': 'Transition Entries'},
        ),
        migrations.RemoveField(
            model_name='transitionentry',
            name='from_state',
        ),
        migrations.RemoveField(
            model_name='transitionentry',
            name='to_state',
        ),
        migrations.AddField(
            model_name='transitionentry',
            name='transition',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='transition', to='metadata.transition'),
            preserve_default=False,
        ),
    ]
