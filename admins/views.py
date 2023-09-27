from django.shortcuts import render,redirect,HttpResponse ,get_object_or_404
from logins.models import user_details
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from .models import Category,books,Coupon
from django.views.decorators.cache import never_cache
from userside.models import Order,OrderItem
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from decimal import Decimal





# Create your views here.
# def handleadmin(request):
#     return render(request ,'baseadmin.html')
@never_cache
def hanglesignin(request):
    
    if request.method == 'POST':
        username=request.POST['email']
        print(username)
        password =request.POST['password']
        try:
            user = user_details.objects.get(username=username)
            print(user)
            password_matched = user.check_password(password)
        except:
            print("dddd")
            return redirect('signin')
        if user and password_matched and user.is_superuser:
            auth.login(request,user)
            return redirect('index')
        else:
            messages.warning(request,'Not a superuser')
            return redirect('signin')
       
    if  not request.user.is_authenticated:
       return render(request,"admintemplate/signin.html")
    else:
    
        return render(request,"admintemplate/index.html")
    
    
@never_cache
@login_required(login_url='signin')
def hangleindex(request):
    # Ensure that the user is a superuser
    if not request.user.is_superuser:
        auth.logout(request)  # Logout non-superusers
        return redirect('signin')

    # Fetch the superuser's details
    obj = user_details.objects.get(is_superuser=True)

    return render(request, "admintemplate/index.html", {'name': obj})

def handleuser(request):
    obj=user_details.objects.exclude(is_superuser = True)
    return render(request,'admintemplate/users.html',{'adm_user':obj})

def handleblock(request,id):
    adm_user = user_details.objects.get(id=id)
    adm_user.is_active =False
    adm_user.save()
    return redirect('users')

def handleunblock(request,id):
    adm_user = user_details.objects.get(id=id)
    adm_user.is_active = True
    adm_user.save()
    return redirect('users')

def handlecategory(request):
    adm_category = Category.objects.all().order_by('id')
    return render(request,'admintemplate/category.html',{'categories':adm_category})

def add_category(request):
    if request.method == 'POST':
        cat_name = request.POST['category_name']
        if cat_name:
            existing_category = Category.objects.filter(name=cat_name).exists()
            if existing_category:
                messages.error(request, "Name is Already Exists.")
            else:
                category = Category(name=cat_name)
                category.save()
                return redirect('category')
    return render(request,'admintemplate/addcategory.html')

def edit_category(request,id):

    cat_obj = Category.objects.get(id=id) 
    if request.method == 'POST':
        edit_name = request.POST.get('edited_name')
        if edit_name is not None:
            try:
                existing_category = Category.objects.get(name=edit_name)
                if existing_category.id != id:
                    messages.info(request, "Category with this name already exists.")
                    return redirect('edit_category/' + str(id))

                cat_obj.name = edit_name
                cat_obj.save()
                return redirect('category')
            except Category.DoesNotExist:
                cat_obj.name = edit_name
                cat_obj.save()
                return redirect('category')
    return render(request, 'admintemplate/editcategory.html', {'cat': cat_obj})

def delete_category(request,id):
    cat_obj = Category.objects.get( id=id)
    cat_obj.delete()
    return redirect('category')

def products(request):
    active_books = books.objects.all()
    
    return render(request,'admintemplate/product.html',{'books_items':active_books})

def add_products(request):
    
    if request.method == "POST":
        title = request.POST.get('book_title')
        category_name= request.POST.get('book_categories')
        author = request.POST.get('book_author')
        active = request.POST.get('book_active')
        handleactive = True if active == 'active' else False
        price = request.POST.get('book_price')
        offer_price = request.POST.get('book_offer_price')
        quantity = request.POST.get('book_quantity')
        discount_percent = request.POST.get('book_discount')
        image = request.FILES.get('book_image')
        discription =request.POST.get('prod_description')
        try:
            category = Category.objects.get(name=category_name)

            new_product = books.objects.create(
                title=title,
                categories=category,
                author=author,
                active=handleactive,
                price=price,
                offer_price=offer_price,
                quantity=quantity,
                discount_percent=discount_percent,
                image=image,
                discription=discription,
            )
            new_product.save()
            return redirect('products')
        except Category.DoesNotExist:
            messages.ERROR(request,"invalid cateroy")
            return redirect('add_products')
    else:
        all_categories = Category.objects.all()
        return render(request,'admintemplate/addproduct.html',{'categories':all_categories})
    
def edit_products(request,book_id):
    edit_books = books.objects.get(id=book_id, deleted=False)
     
    if request.method == "POST":
        title = request.POST.get('edit_title')
        category_name= request.POST.get('edit_categories')
        author = request.POST.get('edit_author')
        active = request.POST.get('edit_active')
        handleactive = True if active == 'active' else False
        price = request.POST.get('edit_price')
        offer_price = request.POST.get('edit_offer_price')
        quantity = request.POST.get('edit_quantity')
        discount_percent = request.POST.get('edit_discount')
        image = request.FILES.get('edit_image')
        discription = request.POST.get('edit_prod_description')
        
        category = Category.objects.get(name=category_name)
        edit_books.title = title
        edit_books.categories = category
        edit_books.author = author
        edit_books.active = handleactive
        edit_books.price = price
        edit_books.offer_price = offer_price
        edit_books.quantity = quantity
        edit_books.discount_percent = discount_percent
        edit_books.image = image
        edit_books.discription = discription
        edit_books.save()
        return redirect('products')
    
    cat=Category.objects.all()
    print(edit_books.discription)
    return render(request, 'admintemplate/editproduct.html', {'edit_book': edit_books, 'categories': cat})
def delete_products(request,book_id):
    delete_pro = books.objects.get(id=book_id)
    delete_pro.soft_delete()
    return redirect('products')

def undelete_products(request,book_id):
    delete_pro = books.objects.get(id=book_id)
    delete_pro.undelete()
    return redirect('products')

def handlelogout(request):
    auth.logout(request)
    return redirect('signin')


    
def userorders(request):
    
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('signin')

    users = user_details.objects.filter(is_superuser=False)
    orders = Order.objects.filter(user__in=users).order_by('-id')

    return render(request, 'admintemplate/userorders.html', {"orders": orders})


def userorderitems(request,id):
   
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('signin')

    order_items = OrderItem.objects.filter(order_id=id).order_by("id")

    return render(request, "admintemplate/userorderitems.html", {"order_items": order_items})

    
def orderstatus(request, id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("'signin'")

    order_items = get_object_or_404(OrderItem, id=id)

    if request.method == "POST":
        order_status = request.POST.get("edited_order_status", "")
        if order_status:
            order_items.order_status = order_status
            order_items.save()
            return redirect('userorders')

    return render(request, "admintemplate/orderstatus.html", {"order_items": order_items})

def coupons(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('signin')

    coupons = Coupon.objects.all()

    return render(request, "admintemplate/coupon.html", {"coupons": coupons})


def add_coupons(request):
    if request.method == "POST":
        coupon_code = request.POST.get("coupon_code", "")
        description = request.POST.get("description", "")
        minimum_amount = int(request.POST.get("minimum_amount", 0))
        discount = Decimal(request.POST.get("discount", 0.0))
        valid_from = timezone.datetime.strptime(
            request.POST.get("valid_from", ""), "%Y-%m-%d"
        ).date()
        valid_to_str = request.POST.get("valid_to")
        valid_to = (
            timezone.datetime.strptime(valid_to_str, "%Y-%m-%d").date()
            if valid_to_str
            else None
        )
        current_date = timezone.now().date()
        is_expired = not (valid_from <= current_date <= valid_to)

        # Create the Coupon object with the correct is_expired value
        coupon = Coupon.objects.create(
            coupon_code=coupon_code,
            description=description,
            minimum_amount=minimum_amount,
            discount=discount,
            valid_from=valid_from,
            valid_to=valid_to,
            is_expired=is_expired,  # Set the correct is_expired value
        )

        return redirect('coupons')

    return render(request, "admintemplate/add_coupon.html")

def edit_coupons(request, id):
    coupon = get_object_or_404(Coupon, id=id)

    if request.method == "POST":
        if "edit_coupon_code" in request.POST:
            edit_coupon_code = request.POST.get("edit_coupon_code")
            coupon.coupon_code = edit_coupon_code

        if "edit_description" in request.POST:
            edit_description = request.POST.get("edit_description")
            coupon.description = edit_description

        if "edit_minimum_amount" in request.POST:
            edit_minimum_amount = request.POST.get("edit_minimum_amount")
            coupon.minimum_amount = edit_minimum_amount

        if "edit_discount" in request.POST:
            edit_discount = request.POST.get("edit_discount")
            coupon.discount = edit_discount

        if "edit_valid_from" in request.POST:
            edit_valid_from = request.POST.get("edit_valid_from")
            coupon.valid_from = edit_valid_from

        if "edit_valid_to" in request.POST:
            edit_valid_to = request.POST.get("edit_valid_to")
            coupon.valid_to = edit_valid_to

        coupon.save()
        return redirect("coupons")

    return render(request, "admintemplate/edit_coupon.html", {"coupon": coupon})


def delete_coupons(request, id):
    coupon = get_object_or_404(Coupon, id=id)
    print(coupon, "aaaaaa")

    coupon.delete()
    return redirect("coupons")
    


    