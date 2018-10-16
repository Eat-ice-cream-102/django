# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Category(models.Model):
    category_no = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'category'

    def __str__(self):
        return self.category_name


class ConfirmString(models.Model):
    c_id = models.AutoField(primary_key=True)
    c_user = models.OneToOneField('Member', models.DO_NOTHING, db_column='c_user', blank=True, null=True)
    code = models.CharField(blank=True, null=True, max_length=256)
    c_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'confirmString'
        ordering = ["-c_time"]
        verbose_name = "確認碼"
        verbose_name_plural = "確認碼"

    def __str__(self):
        return self.c_user.member_name + ":   " + self.code


class InOrOut(models.Model):
    come_time = models.DateTimeField(primary_key=True)
    left_time = models.DateTimeField(blank=True, null=True)
    phone_number = models.ForeignKey('Member', models.DO_NOTHING, db_column='phone_number', blank=True, null=True)
    satisfaction = models.IntegerField(null=True, blank=True)
    inorout = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'inorout'

    def __str__(self):
        return str(self.come_time) + "： " + self.phone_number.member_name


class Member(models.Model):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    phone_number = models.CharField(primary_key=True, max_length=10)
    member_name = models.CharField(max_length=128)
    line_account = models.CharField(unique=True, max_length=255, blank=True, null=True)
    birthdate = models.DateTimeField(blank=True, null=True)
    e_mail = models.CharField(unique=True, max_length=255, blank=True, null=True)
    credit_card = models.CharField(max_length=50, blank=True, null=True)
    photo = models.ImageField(upload_to='profile_image', blank=True)
    member_password = models.CharField(max_length=255, blank=True, null=True)
    has_confirmed = models.BooleanField(default=False)
    c_time = models.DateTimeField(auto_now_add=True)
    has_photo = models.BooleanField(default=False)
    gender = models.CharField(max_length=32, choices=gender, default="男")

    class Meta:
        managed = True
        db_table = 'member'

    def __str__(self):
        return self.member_name


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    category_no = models.ForeignKey(Category, models.DO_NOTHING, db_column='category_no', blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)
    product_url = models.CharField(max_length=255, blank=True, null=True)
    picture_url = models.CharField(max_length=255, blank=True, null=True)
    re_product_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'product'

    def __str__(self):
        return self.product_name


class Purchase(models.Model):
    purchase_no = models.AutoField(primary_key=True)
    come_time = models.ForeignKey(InOrOut, models.DO_NOTHING, db_column='come_time', blank=True, null=True)
    product = models.ForeignKey(Product, models.DO_NOTHING, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    satisfaction = models.IntegerField(blank=True, null=True)
    neededcall = models.IntegerField(blank=True, default=0)

    class Meta:
        managed = True
        db_table = 'purchase'

    def __str__(self):
        return str(self.purchase_no) + ": " + str(self.come_time)
