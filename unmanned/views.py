from django.shortcuts import render, HttpResponse
from django.shortcuts import redirect
from . import models, forms
import hashlib
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
import re
import base64
import os
import datetime
from django.db.models import Sum
from django.views.decorators.cache import cache_page


# Create your views here.


def index(request):
    if request.session.get('is_login', None):
        hot_product = models.Purchase.objects.values('product__product_url', 'product__picture_url').\
            annotate(sum_quantity=Sum('quantity')).order_by('-sum_quantity')[:3]
    else:
        pass
    return render(request, 'client/index.html', locals())


def login(request):
    if request.session.get('is_login', None):
        return redirect("/index/")
    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        message = "請檢查填寫內容！"
        if login_form.is_valid():
            user_email = login_form.cleaned_data['user_email']

            password = login_form.cleaned_data['password']
            try:
                user = models.Member.objects.get(e_mail=user_email)

                if not user.has_confirmed:
                    message = "該用戶還未通過信箱認證！"
                    return render(request, 'client/login.html', locals())
                if user.member_password == hash_code(password):  # 哈希值和数据库内的值进行比对
                    request.session['is_login'] = True
                    request.session['user_id'] = user.phone_number
                    request.session['user_email'] = user.e_mail
                    request.session['user_name'] = user.member_name
                    request.session['user_img'] = user.photo.url
                    return redirect('/index/')
                else:
                    message = "密碼不正確！"
            except:
                message = "此用戶不存在！"

        return render(request, 'client/login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'client/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。
        return redirect("/index/")
    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST, request.FILES)
        message = "請檢查填寫內容！"
        if register_form.is_valid():  # 获取数据
            email = register_form.cleaned_data['email']
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            sex = register_form.cleaned_data['sex']
            phone_number = register_form.cleaned_data['phone_number']
            image = register_form.cleaned_data['image']
            birthday = register_form.cleaned_data['birthday']
            if password1 != password2:  # 判断两次密码是否相同
                message = "兩次輸入的密碼不同！"
                return render(request, 'client/register.html', locals())
            else:
                same_email_user = models.Member.objects.filter(e_mail=email)
                if same_email_user:  # 信箱唯一
                    message = '該信箱已被使用，請選擇其他信箱！'
                    return render(request, 'client/register.html', locals())
                same_phone_number_user = models.Member.objects.filter(phone_number=phone_number)
                if same_phone_number_user:  # 電話唯一
                    message = '該電話已經被使用，請選擇其他電話！'
                    return render(request, 'client/register.html', locals())
                if birthday > datetime.date.today():  # 電話唯一
                    message = '生日不能超過今天日期！'
                    return render(request, 'client/register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = models.Member()
                new_user.member_name = username
                new_user.member_password = hash_code(password1)  # 使用加密密码
                new_user.e_mail = email
                new_user.gender = sex
                new_user.photo = image
                new_user.phone_number = phone_number
                new_user.birthdate = birthday
                new_user.save()
                code = make_confirm_string(new_user)

                send_email(email, code)
                message = '請前往註冊信箱，進行認證！'
                return render(request, 'client/confirm.html', locals())  # 跳转到等待邮件确认页面。
    register_form = forms.RegisterForm()
    return render(request, 'client/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/index/")  # logout後，redirect會將頁面重新導向index


def hash_code(s, salt='mysite4'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.member_name, now)
    models.ConfirmString.objects.create(code=code, c_user=user, )
    return code


def send_email(email, code):
    from django.core.mail import EmailMultiAlternatives

    subject = '来自吃冰102的註冊信件'

    text_content = '''感谢註冊www.cb102.com，這裡充滿各種高大上的物品！\
                    如果你看到这條消息，說明您的信箱服務器不提供HTML連接，請盡速聯繫管理員！'''

    html_content = '''
                    <p>感謝註冊<a href="https://{}/confirm/?code={}" target=blank>www.cb102.com</a>，\
                    這裡是吃冰102的線上網站，註冊后可享受高科技購物！</p>
                    <p>請點擊鏈接完成註冊！</p>
                    <p>此鏈接有效期為{}天！</p>
                    '''.format(settings.ALLOWED_HOSTS[0] + ':8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '無效的確認請求!'
        return render(request, 'client/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的信箱已過期！請重新註冊!'
        return render(request, 'client/confirm.html', locals())
    else:
        confirm.c_user.has_confirmed = True
        confirm.c_user.save()
        confirm.delete()
        message = '感謝您的認證，請使用帳號登入！'
        return render(request, 'client/confirm.html', locals())


def get_record(request):
    if not request.session.get('is_login', None):
        return redirect("/index/")
    records = models.InOrOut.objects.filter(phone_number=request.session.get('user_id')).order_by('-order_date') \
        .prefetch_related('orderdetail_set')

    return render(request, 'client/record.html', locals())


def get_profile(request):
    if not request.session.get('is_login', None):
        return redirect("/index/")
    user_profile = models.Member.objects.filter(phone_number=request.session.get('user_id'))
    records = models.InOrOut.objects.filter(phone_number=request.session.get('user_id')).order_by('-come_time') \
        .prefetch_related('purchase_set')
    return render(request, 'client/profile.html', locals())


def take_pic(request):
    # import os
    # try:
    #     path = "/Users/jiangbifeng/work/django2/unmanned/dataset/{}".format(request.session.get('user_id'))
    #     os.mkdir(path)
    # except:
    #     pass
    # os.system('/Users/jiangbifeng/.pyenv/versions/3.6.5/bin/python '
    #           '/Users/jiangbifeng/work/django2/unmanned/take_face_pictures.py '
    #           '--cascade haarcascade_frontalface_default.xml --output {}'.format(path))
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    return render(request, 'client/take_pic.html')


@csrf_exempt
def upload_image(request):
    path = os.path.join(settings.BASE_DIR, "dataset")
    try:
        path = str(path) + "/" + request.session.get('user_id')
        os.mkdir(path)
    except:
        pass
    try:
        data = json.loads(request.POST['data'])
        data = list(map(lambda x: re.sub('data:image/png;base64,', '', x), data))
        data = list(map(lambda x: base64.b64decode(x), data))
        for i, img_data in enumerate(data):
            with open("%s/%s.jpg" % (path, i), "wb") as img_file:
                img_file.write(img_data)
        has_pic = models.Member.objects.get(phone_number=request.session.get('user_id'))
        has_pic.has_photo = True
        has_pic.save()
    except:
        pass

    return HttpResponse("uploaded")


def test_page(request):
    pass
    return render(request, "client/test.html")


# ____（分割線）以下為admin端____


def admin_report(request):
    category = models.Category.objects.all()
    member = models.Member.objects.all()
    purchase = models.Product.objects.raw("""select case  count(quantity)
                                                          when 0 then 0
                                                          else sum(quantity) 
                                                          end qty,
                                                    product_name,
                                                    case  count(quantity)
                                                          when 0 then 0
                                                          else sum(quantity*price)
                                                          end total,
                                                    product_name,
                                                    product.product_id ,count(quantity) as times
                                             from product
                                             left join purchase
                                             on purchase.product_id = product.product_id
                                             group by product_id                                            
                                             order by total desc """)
    return render(request, 'admin_page/admin_report.html', locals())


@csrf_exempt
def sales(request):
    # 產品類別
    num = request.GET["get_category"]
    # 日期
    start_date = request.GET["datetime"]
    end_date = request.GET["endtime"]
    # check box 是否被勾選
    order_time = None
    order_money = None
    if request.GET.getlist("time"):
        order_time = request.GET["time"]
    if request.GET.getlist("money"):
        order_money = request.GET["money"]
    # 全選
    if num == '0':
        # 時間排序
        if order_time is not None:
            purchase = models.Purchase.objects.select_related("come_time", "product").filter(come_time__gte=start_date,
                                                                                             come_time__lte=end_date).all(). \
                order_by('-come_time')
        # 金錢排序
        elif order_money is not None:
            purchase = models.Purchase.objects.select_related("come_time", "product").filter(come_time__gte=start_date,
                                                                                             come_time__lte=end_date).all(). \
                order_by('product__price')
        # 不排序
        else:
            purchase = models.Purchase.objects.select_related("come_time", "product").filter(come_time__gte=start_date,
                                                                                             come_time__lte=end_date).all()

    else:
        # 時間排序
        if order_time is not None:
            purchase = models.Purchase.objects.select_related("come_time", "product").filter(come_time__gte=start_date,
                                                                                             come_time__lte=end_date,
                                                                                             product__category_no=num).all()
        # 金錢排序
        elif order_money is not None:
            purchase = models.Purchase.objects.select_related("come_time", "product").filter(come_time__gte=start_date,
                                                                                             come_time__lte=end_date,
                                                                                             product__category_no=num).all(). \
                order_by('-product__price')
        # 不排序
        else:
            purchase = models.Purchase.objects.select_related("come_time", "product").filter(come_time__gte=start_date,
                                                                                             come_time__lte=end_date,
                                                                                             product__category_no=num).all()
    return render(request, 'admin_page/sales.html', {'purchase': purchase})


@csrf_exempt
def stock(request):
    num = request.GET["get_category"]
    # check box是否被勾選
    order_time = None
    order_money = None
    if request.GET.getlist("time"):
        order_time = request.GET["time"]
    if request.GET.getlist("money"):
        order_money = request.GET["money"]
    # 全選
    if num == "0":
        # 時間排序
        if order_time is not None:
            produce = models.Product.objects.all().select_related("category_no").order_by("stock")
        # 金錢排序
        elif order_money is not None:
            produce = models.Product.objects.all().select_related("category_no").order_by("price")
        # 不排序
        else:
            produce = models.Product.objects.all()
    else:
        # 時間排序
        if order_time is not None:
            produce = models.Product.objects.select_related("category_no").filter(category_no=num).all().order_by(
                "stock")
        # 金錢排序
        elif order_money is not None:
            produce = models.Product.objects.select_related("category_no").filter(category_no=num).all().order_by(
                "price")
        # 不排序
        else:
            produce = models.Product.objects.select_related("category_no").filter(category_no=num).all()
    return render(request, 'admin_page/stock.html', {'produce': produce})


@csrf_exempt
def member_information(request):
    # 產品類別
    num = request.GET["get_category"]
    # 會員編號
    member = request.GET["get_member"]

    # 日期
    start_date = request.GET["datetime"]
    end_date = request.GET["endtime"]

    # check box是否被勾選
    order_time = None
    order_money = None
    if request.GET.getlist("time"):
        order_time = request.GET["time"]
    if request.GET.getlist("money"):
        order_money = request.GET["money"]

    # 種類=全部 會員＝全部
    if num == '0' and member == '0':
        # 時間排序
        if order_time is not None:
            purchase = models.Purchase.objects.select_related("come_time", "product").filter(come_time__gte=start_date,
                                                                                             come_time__lte=end_date).all(). \
                order_by('-come_time')
        # 金錢排序
        elif order_money is not None:
            purchase = models.Purchase.objects.select_related("come_time", "product").filter(come_time__gte=start_date,
                                                                                             come_time__lte=end_date).all(). \
                order_by('product__price')
        # 不排序
        else:
            purchase = models.Purchase.objects.select_related("come_time", "product").filter(come_time__gte=start_date,

                                                                                             come_time__lte=end_date).all()
    # 種類=全部 會員!＝全部
    elif num == "0" and member != "0":
        # 時間排序
        if order_time is not None:
            purchase = models.Purchase.objects.select_related("come_time", "product").filter(come_time__gte=start_date,
                                                                                             come_time__lte=end_date,
                                                                                             come_time__phone_number=member
                                                                                             ).all().order_by(
                '-come_time')
        # 金錢排序
        elif order_money is not None:
            purchase = models.Purchase.objects.select_related("come_time", "product").filter(come_time__gte=start_date,
                                                                                             come_time__lte=end_date,
                                                                                             come_time__phone_number=member). \
                all().order_by('product__price')
        # 不排序
        else:
            purchase = models.Purchase.objects.select_related("come_time", "product").filter(come_time__gte=start_date,
                                                                                             come_time__lte=end_date,
                                                                                             come_time__phone_number=member). \
                all()
    # 種類!=全部 會員＝全部
    elif num != "0" and member == "0":
        # 時間排序
        if order_time is not None:
            purchase = models.Purchase.objects.select_related("come_time", "product").filter(come_time__gte=start_date,
                                                                                             come_time__lte=end_date,
                                                                                             product__category_no=num). \
                all().order_by('-come_time')
        # 金錢排序
        elif order_money is not None:
            purchase = models.Purchase.objects.select_related("come_time", "product").filter(come_time__gte=start_date,
                                                                                             come_time__lte=end_date,
                                                                                             product__category_no=num). \
                all().order_by('produce__price')
        # 不排序
        else:
            purchase = models.Purchase.objects.select_related("come_time", "product").filter(come_time__gte=start_date,
                                                                                             come_time__lte=end_date,
                                                                                             product__category_no=num). \
                all()
    else:
        # 時間排序
        if order_time is not None:
            purchase = models.Purchase.objects.select_related("come_time", "product").filter(come_time__gte=start_date,
                                                                                             come_time__lte=end_date,
                                                                                             product__category_no=num,
                                                                                             come_time__phone_number=member). \
                all().order_by('-come_time')
        # 金錢排序
        elif order_money is not None:
            purchase = models.Purchase.objects.select_related("come_time", "product").filter(come_time__gte=start_date,
                                                                                             come_time__lte=end_date,
                                                                                             product__category_no=num,
                                                                                             come_time__phone_number=member). \
                all().order_by('product__price')
        # 不排序
        else:
            purchase = models.Purchase.objects.select_related("come_time", "product").filter(come_time__gte=start_date,
                                                                                             come_time__lte=end_date,
                                                                                             product__category_no=num,
                                                                                             come_time__phone_number=member). \
                all()

    return render(request, 'admin_page/member_information.html', {'purchase': purchase})


@csrf_exempt
def member_analysis(request):
    # 取得會員編號
    member = request.GET["get_member"]
    # 取得下拉式選單（大於/小於/等於/不限）
    money = request.GET["select_money"]
    times = request.GET["select_times"]
    # 取得值
    if money != "0":
        compare_money = request.GET["how_much_money"]
    if times != "0":
        compare_times = request.GET["times"]
    # 大於/小於/等於/不限
    operate = [" ", "=", "<", ">"]
    # having 語法
    # 金額!=不限 次數=不限
    if money != "0" and times == "0":
        having = """ having sum(quantity*price) {} {}""".format(operate[int(money)], compare_money)
    # 金額=不限 次數!=不限
    elif money == "0" and times != "0":
        having = """ having count(inorout.come_time) {} {}""".format(operate[int(times)], compare_times)
    # 金額!=不限 次數!=不限
    elif money != "0" and times != "0":
        having = """ having sum(quantity*price) {} {} and count(inorout.come_time) {} {}""".format(operate[int(money)],
                                                                                                   compare_money,
                                                                                                   operate[int(times)],
                                                                                                   compare_times)
    else:
        having = None
    # 全部會員資料
    if member == "0":
        if money == "0" and times == "0":
            member_query = models.Member.objects.raw("""select sum(quantity*price) as total,
                                                        member.phone_number,
                                                        member_name ,
                                                        count(inorout.come_time) as times
                                                from purchase 
                                                left join inorout 
                                                on inorout.come_time=purchase.come_time 
                                                left join product 
                                                on purchase.product_id=product.product_id 
                                                left join member
                                                on member.phone_number=inorout.phone_number 
                                                group by inorout.phone_number
                                                order by inorout.phone_number
                                                    """)

        else:
            member_query = models.Member.objects.raw("""select sum(quantity*price) as total,
                                                        member.phone_number,
                                                        member_name ,
                                                        count(inorout.come_time) as times 
                                                 from purchase 
                                                 left join inorout 
                                                 on inorout.come_time=purchase.come_time 
                                                 left join product 
                                                 on purchase.product_id=product.product_id 
                                                 left join member
                                                 on member.phone_number=inorout.phone_number 
                                                 group by inorout.phone_number
                                                 {}
                                                 order by inorout.phone_number""".format(having))

    else:
        if money == "0" and times == "0":
            member_query = models.Member.objects.raw("""select sum(quantity*price) as total,
                                                        member.phone_number,
                                                        member_name ,
                                                        count(inorout.come_time) as times 
                                                 from purchase 
                                                 left join inorout 
                                                 on inorout.come_time=purchase.come_time 
                                                 left join product 
                                                 on purchase.product_id=product.product_id 
                                                 left join member
                                                 on member.phone_number=inorout.phone_number
                                                 where inorout.phone_number= {} 
                                                 group by inorout.phone_number 
                                                 order by inorout.phone_number """.format(member))
        else:
            member_query = models.Member.objects.raw("""select sum(quantity*price) as total,
                                                        member.phone_number,
                                                        member_name ,           
                                                        count(inorout.come_time) as times 
                                                 from purchase 
                                                 left join inorout 
                                                 on inorout.come_time=purchase.come_time 
                                                 left join product 
                                                 on purchase.product_id=product.product_id 
                                                 left join member
                                                 on member.phone_number=inorout.phone_number
                                                 where inorout.phone_number= {} 
                                                 group by inorout.phone_number 
                                                 {} order by inorout.phone_number""".format(member, having))

    return render(request, 'admin_page/member_analysis.html', {'member': member_query})
