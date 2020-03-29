# Generated by Django 3.0.4 on 2020-03-29 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Carrier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carrier_name', models.CharField(default='FedEx', max_length=200, unique=True)),
                ('test', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='CanadaPostSettings',
            fields=[
                ('carrier_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.Carrier')),
                ('username', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('customer_number', models.CharField(max_length=200)),
                ('contract_id', models.CharField(blank=True, default='', max_length=200)),
            ],
            options={
                'verbose_name': 'Canada Post Setting',
                'verbose_name_plural': 'Canada Post Settings',
                'db_table': 'canada-post-settings',
            },
            bases=('core.carrier',),
        ),
        migrations.CreateModel(
            name='DHLSettings',
            fields=[
                ('carrier_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.Carrier')),
                ('site_id', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('account_number', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'DHL Setting',
                'verbose_name_plural': 'DHL Settings',
                'db_table': 'dhl-settings',
            },
            bases=('core.carrier',),
        ),
        migrations.CreateModel(
            name='FedexSettings',
            fields=[
                ('carrier_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.Carrier')),
                ('user_key', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('meter_number', models.CharField(max_length=200)),
                ('account_number', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'FedEx Setting',
                'verbose_name_plural': 'FedEx Settings',
                'db_table': 'fedex-settings',
            },
            bases=('core.carrier',),
        ),
        migrations.CreateModel(
            name='PurolatorSettings',
            fields=[
                ('carrier_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.Carrier')),
                ('user_token', models.CharField(max_length=200)),
                ('account_number', models.CharField(max_length=200)),
                ('language', models.CharField(default='en', max_length=200)),
            ],
            options={
                'verbose_name': 'Purolator Setting',
                'verbose_name_plural': 'Purolator Settings',
                'db_table': 'purolator-settings',
            },
            bases=('core.carrier',),
        ),
        migrations.CreateModel(
            name='UPSSettings',
            fields=[
                ('carrier_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.Carrier')),
                ('username', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('access_license_number', models.CharField(max_length=200)),
                ('account_number', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'UPS Setting',
                'verbose_name_plural': 'UPS Settings',
                'db_table': 'ups-settings',
            },
            bases=('core.carrier',),
        ),
    ]
