# Generated by Django 2.1 on 2018-10-06 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_no', models.AutoField(primary_key=True, serialize=False)),
                ('category_name', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'category',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ConfirmString',
            fields=[
                ('c_id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.IntegerField(blank=True, null=True)),
                ('c_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'confirmString',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='InOrOut',
            fields=[
                ('come_time', models.DateTimeField(primary_key=True, serialize=False)),
                ('left_time', models.DateTimeField(blank=True, null=True)),
                ('inorout', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'inorout',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('phone_number', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('member_name', models.CharField(max_length=20)),
                ('line_account', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('birthdate', models.DateTimeField(blank=True, null=True)),
                ('e_mail', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('credit_card', models.CharField(blank=True, max_length=50, null=True)),
                ('photo', models.CharField(blank=True, max_length=255, null=True)),
                ('member_password', models.CharField(blank=True, max_length=255, null=True)),
                ('has_confirmed', models.IntegerField(blank=True, null=True)),
                ('c_time', models.DateTimeField(blank=True, null=True)),
                ('has_photo', models.IntegerField(blank=True, null=True)),
                ('gender', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'member',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(blank=True, max_length=50, null=True)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('stock', models.IntegerField(blank=True, null=True)),
                ('product_url', models.CharField(blank=True, max_length=255, null=True)),
                ('picture_url', models.CharField(blank=True, max_length=255, null=True)),
                ('re_product_id', models.IntegerField(blank=True, null=True)),
                ('category_no', models.ForeignKey(blank=True, db_column='category_no', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='unmanned.Category')),
            ],
            options={
                'db_table': 'product',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('purchase_no', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('satisfaction', models.IntegerField(blank=True, null=True)),
                ('neededcall', models.IntegerField(blank=True, null=True)),
                ('come_time', models.ForeignKey(blank=True, db_column='come_time', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='unmanned.InOrOut')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='unmanned.Product')),
            ],
            options={
                'db_table': 'purchase',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='inorout',
            name='phone_number',
            field=models.ForeignKey(blank=True, db_column='phone_number', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='unmanned.Member'),
        ),
        migrations.AddField(
            model_name='confirmstring',
            name='c_user',
            field=models.ForeignKey(blank=True, db_column='c_user', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='unmanned.Member'),
        ),
    ]
