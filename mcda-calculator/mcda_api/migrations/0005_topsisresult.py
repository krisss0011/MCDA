# Generated by Django 5.1.4 on 2024-12-22 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcda_api', '0004_ahpresult_cachedresults'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopsisResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criteria_weights', models.JSONField()),
                ('ranked_companies', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'topsis_results',
            },
        ),
    ]
