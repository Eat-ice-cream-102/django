# Generated by Django 2.1 on 2018-10-06 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('unmanned', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='confirmstring',
            options={'managed': True, 'ordering': ['-c_time'], 'verbose_name': '確認碼', 'verbose_name_plural': '確認碼'},
        ),
        migrations.AlterField(
            model_name='confirmstring',
            name='c_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='confirmstring',
            name='c_user',
            field=models.OneToOneField(blank=True, db_column='c_user', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='unmanned.Member'),
        ),
        migrations.AlterField(
            model_name='confirmstring',
            name='code',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='c_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='e_mail',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='gender',
            field=models.CharField(choices=[('male', '男'), ('female', '女')], default='男', max_length=32),
        ),
        migrations.AlterField(
            model_name='member',
            name='has_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='member',
            name='has_photo',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='member',
            name='member_name',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='member',
            name='photo',
            field=models.ImageField(blank=True, upload_to='profile_image'),
        ),
    ]
