# Generated by Django 4.2 on 2024-09-26 09:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('left_operand', models.CharField(max_length=255)),
                ('operator', models.CharField(choices=[('>', 'Greater Than'), ('<', 'Less Than'), ('==', 'Equal'), ('!=', 'Not Equal'), ('>=', 'Greater or Equal'), ('<=', 'Less or Equal')], max_length=10)),
                ('right_operand', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Condition',
                'verbose_name_plural': 'Conditions',
                'db_table': 'condition',
                'ordering': ['left_operand'],
            },
        ),
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255, unique=True)),
                ('value', models.FloatField()),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Configuration',
                'verbose_name_plural': 'Configurations',
                'db_table': 'configuration',
                'ordering': ['key'],
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'State',
                'verbose_name_plural': 'States',
                'db_table': 'state',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Transition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('conditions', models.ManyToManyField(blank=True, to='database.condition')),
                ('from_state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_state', to='database.state')),
                ('to_state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_state', to='database.state')),
            ],
            options={
                'verbose_name': 'Transition',
                'verbose_name_plural': 'Transitions',
                'db_table': 'transition',
                'ordering': ['from_state', 'to_state'],
                'unique_together': {('from_state', 'to_state')},
            },
        ),
    ]
