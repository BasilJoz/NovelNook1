from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Cart, CartItems
from admins.models import books, Coupon
from logins.models import user_details
from logins.models import Address
from .models import Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
import os
from decimal import Decimal, ROUND_HALF_UP
import razorpay


# Create your views here.
@login_required(login_url="login")
def cart(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    cart_item = CartItems.objects.filter(cart=cart)
    total_price = sum(item.quantity * item.book.price for item in cart_item)
    cart_coupon = cart.coupon
    if request.method == "POST":
        coupon_code = request.POST.get("coupon_code")
        try:
            coupon = Coupon.objects.get(coupon_code=coupon_code)
            if not cart_coupon and total_price >= coupon.minimum_amount:
                cart.coupon = coupon
                cart.save()
                messages.success(request, "Coupon added successfully")
                return redirect("cart")
            elif cart_coupon:
                messages.warning(request, "You have already used a coupon")
            else:
                messages.warning(
                    request, "Not eligible for the current price, add more items"
                )
        except Coupon.DoesNotExist:
            messages.warning(request, "Please enter a valid coupon")

    coupon_discount = cart_coupon.discount if cart_coupon else 0
    final_total = total_price - coupon_discount
    return render(
        request,
        "usertemplate/cart.html",
        {
            "cart_items": cart_item,
            "total_price": total_price,
            "coupon_discount": coupon_discount,
            "final_total": final_total,
            "cart_coupon": cart_coupon,
        },
    )


from django.http import JsonResponse

# ...


def update_cart_item_quantity(request):
    # Get the cart item
    # Check if the request is a POST request
    if request.method == "POST":
        item_id = int(request.POST["item_id"])
        quantity = int(request.POST["quantity"])
        cart_item = get_object_or_404(CartItems, id=item_id)

        stock = cart_item.book.quantity
        cart_item_quantity = cart_item.quantity

        if cart_item_quantity <= 1 and quantity == -1:
            return JsonResponse({"success": False, "message": "Cannot delete"})

        if cart_item_quantity >= stock and quantity == 1:
            return JsonResponse({"success": False, "message": "Max. Limit excceeded"})

        # Update the quantity of the cart item
        if quantity:
            cart_item.quantity += quantity
            cart_item.save()

            # Calculate the updated total price (if needed)
            cart = cart_item.cart
            cart_item_list = CartItems.objects.filter(cart=cart)
            total_price = sum(
                item.quantity * item.book.price for item in cart_item_list
            )
            updated_quantity = cart_item.quantity
            product_price = cart_item.book.price

            # Return a JSON response with the updated data
            return JsonResponse(
                {
                    "success": True,
                    "total_price": total_price,
                    "quantity": updated_quantity,
                    "product_price": product_price,
                }
            )

    # Return a JSON response for errors (if needed)
    return JsonResponse({"success": False, "error": "Invalid request"})


@login_required(login_url="login")
def add_cart(request, book_id):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    book = get_object_or_404(books, id=book_id)
    cart_items, item_created = CartItems.objects.get_or_create(
        cart=cart, book=book, defaults={"quantity": 1}
    )
    cart_items.save()
    return redirect("hanldesingleproduct", product_id=book_id)


def delete_cart_item(request, item_id):
    user = request.user
    cart = get_object_or_404(Cart, user=user)
    cart_item = get_object_or_404(CartItems, id=item_id, cart=cart)

    # Remove the item from the cart
    cart_item.delete()

    return redirect("cart")


# profile handleing section


@login_required(login_url="login")
def userprofile(request):
    user = request.user
    print(user, "ukyfyuuu")

    if "first_name" in request.POST:
        edited_fist_name = request.POST["first_name"]
        user.first_name = edited_fist_name
        user.save()
    if "last_name" in request.POST:
        edited_last_name = request.POST["last_name"]
        user.last_name = edited_last_name
        user.save()
    if "gender" in request.POST:
        edited_gender = request.POST["gender"]
        user.gender = edited_gender
        user.save()
    if "age" in request.POST:
        edited_age = request.POST["age"]
        user.age = edited_age
        user.save()
    if "email" in request.POST:
        edited_email = request.POST["email"]
        user.email = edited_email
        user.save()

    return render(
        request,
        "usertemplate/userprofile.html",
        {
            "username": user.username,
            "email": user.email,
            "phone": user.phone_number,
            "age": user.age,
            "gender": user.gender,
            "first_name": user.first_name,
            "last_name": user.last_name,
        },
    )


def useraddress(request):
    if not request.user.is_authenticated:
        return redirect("login")
    user = request.user
    address = Address.objects.filter(user=user)

    return render(request, "usertemplate/useraddress.html", {"addresses": address})


def add_address(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":
        print("dskjhfsdaklhaslkhfaslkhklasfh")
        housename_companyname = request.POST.get("Housename_companyname")
        post_office = request.POST.get("Post_office")
        street = request.POST.get("Street")
        city = request.POST.get("City")
        state = request.POST.get("State")
        country = request.POST.get("Country")
        pin_code = request.POST.get("Pin_code")

        address = Address(
            user=request.user,
            name=housename_companyname,
            postoffice=post_office,
            street=street,
            city=city,
            state=state,
            country=country,
            pin_code=pin_code,
        )
        address.save()
        print("Saved Address Details:")
        print("Name:", address.name)
        print("Post Office:", address.postoffice)
        print("Street:", address.street)
        print("City:", address.city)
        print("State:", address.state)
        print("Country:", address.country)
        print("Pin Code:", address.pin_code)

        next_url = request.GET.get("next", None)

        if next_url:
            return redirect(next_url)
        else:
            return redirect("useraddress")

    return render(request, "usertemplate/add_address.html")


def edit_address(request, edit_id):
    if not request.user.is_authenticated:
        return redirect("login")

    address = get_object_or_404(Address, id=edit_id, user=request.user)

    if request.method == "POST":
        housename_companyname = request.POST.get("Edited_Housename_companyname")
        post_office = request.POST.get("Edited_Post_office")
        street = request.POST.get("Edited_Street")
        city = request.POST.get("Edited_City")
        state = request.POST.get("Edited_State")
        country = request.POST.get("Edited_Country")
        pin_code = request.POST.get("Edited_Pin_code")

        address.name = housename_companyname
        address.postoffice = post_office
        address.street = street
        address.city = city
        address.state = state
        address.country = country
        address.pin_code = pin_code
        address.save()

        next_url = request.GET.get("next", None)

        if next_url:
            print(next_url)
            return redirect(next_url)
        else:
            return redirect("useraddress")

    return render(request, "usertemplate/edit_address.html", {"address": address})


def delete_address(request, del_id):
    address = get_object_or_404(Address, id=del_id)
    address.delete()
    return redirect("useraddress")


def checkout(request):
    if not request.user.is_authenticated:
        return redirect("user_login")

    user = request.user
    addresses = Address.objects.filter(user=user)

    selected_address_id = None
    # default_address = addresses.order_by("-id").first()
    # print(default_address,'dfakkahjsflkah')

    if request.method == "POST":
        print("rrrrr")
        selected_address_id = request.POST.get("selected_address")
        print(selected_address_id, "hgfjhgfhfbasil")

        return redirect(
            "payment",
            address_id=selected_address_id,
        )
    else:
        return render(
            request,
            "usertemplate/checkout.html",
            {
                "addresses": addresses,
                # "default_address": default_address,
            },
        )


def payment(request, address_id):
    if not request.user.is_authenticated:
        return redirect("login")

    user = request.user
    address = Address.objects.get(id=address_id)
    address_id = address.id
    cart = Cart.objects.get(user=user)
    cart_coupon = cart.coupon
    coupon_discount = cart_coupon.discount if cart_coupon else 0
    cart_items = CartItems.objects.filter(cart=cart)

    total_price = 0
    final_total = 0

    for item in cart_items:
        item.offer_price = item.book.price
        item.total_price_each = item.offer_price * item.quantity
        total_price += item.total_price_each

        if cart_coupon:
            total_price = total_price - coupon_discount
        else:
            pass

    final_total = total_price + 50

    if request.method == "GET":
        razorpay_client = razorpay.Client(
            auth=(
                os.environ.get("RAZORPAY_KEY_ID"),
                os.environ.get("RAZORPAY_KEY_SECRET"),
            )
        )

        order_data = {
            "amount": int(final_total * 100),  # Amount in paise
            "currency": "INR",
            "payment_capture": 1,  # Auto-capture the payment
        }

        try:
            payment = razorpay_client.order.create(data=order_data)
            print(payment, "yyyyyyyyrrr")
        except Exception as e:
            print(f"Razorpay API error: {str(e)}")

        context = {
            "address_id": address_id,
            "total_price": total_price,
            "final_total": final_total,
        }
        return render(request, "usertemplate/payment.html", context)

    if request.method == "POST":
        if "cash_on_delivery" in request.POST:
            payment_method_id_1 = request.POST.get("cash_on_delivery")

            if address and payment_method_id_1:
                payment_method = "Cash On Delivery"

                order = Order.objects.create(
                    user=user,
                    address=address,
                    payment_method=payment_method,
                    order_date=timezone.now(),
                    total_price=total_price,
                    total_price_shipping=final_total,
                )

                for item in cart_items:
                    book = item.book
                    quantity = item.quantity

                    if book.quantity >= quantity:
                        book.quantity -= quantity
                        book.save()

                        OrderItem.objects.create(
                            order=order,
                            product=book,
                            quantity=quantity,
                        )
                    else:
                        print("Insufficient stock...")
                        pass

                cart.coupon = None
                cart.save()
                cart_items.delete()

                return redirect(
                    "order_summary",
                    address_id=address_id,
                    order_id=order.id,
                )


def razor(request, address_id, final_total):
    try:
        user = request.user
        address = Address.objects.get(id=address_id)
        cart = Cart.objects.get(user=user)
        cart_coupon = cart.coupon
        coupon_discount = cart_coupon.discount if cart_coupon else 0
        cart_items = CartItems.objects.filter(cart=cart)

        total_price = 0

        for item in cart_items:
            item.offer_price = item.book.price
            item.total_price_each = item.offer_price * item.quantity
            total_price += item.total_price_each

        if cart_coupon:
            total_price -= coupon_discount

        final_total = total_price + 50

        if address:
            order = Order.objects.create(
                user=user,
                address=address,
                payment_method="Razor Pay",
                order_date=timezone.now(),
                total_price=total_price,
                total_price_shipping=final_total,
            )

            for item in cart_items:
                book = item.book
                quantity = item.quantity

                if book.quantity >= quantity:
                    book.quantity -= quantity
                    book.save()

                    OrderItem.objects.create(
                        order=order,
                        product=book,
                        quantity=quantity,
                    )
                else:
                    messages.error(request, "Insufficient stock for one or more items.")
                    

            cart.coupon = None
            cart.save()
            cart_items.delete()

            return redirect(
                'order_summary',
                address_id=address.id,
                order_id=order.id,
            )
        else:
            messages.error(request, "Selected address not found.")
            
    except Address.DoesNotExist:
        messages.error(request, "Address does not exist.")
        pass
    except Cart.DoesNotExist:
        messages.error(request, "Cart does not exist.")
        pass
        

def order_summary(request, address_id, order_id):
    if not request.user.is_authenticated:
        return redirect("login")

    user = request.user
    address = Address.objects.get(id=address_id)
    username = user.username

    orders = Order.objects.get(id=order_id, address=address)
    order_items = OrderItem.objects.filter(order=orders)

    context = {
        "address": address,
        "username": username,
        "orders": orders,
        "order_items": order_items,
    }

    return render(request, "usertemplate/order_summary.html", context)


def my_orders(request):
    if not request.user.is_authenticated:
        return redirect("login")

    user = request.user
    orders = Order.objects.filter(user=user)

    order_items = OrderItem.objects.filter(order__in=orders).order_by("-id")

    return render(request, "usertemplate/my_orders.html", {"order_items": order_items})


def cancel_order(request, order_id, product_id):
    order = get_object_or_404(Order, id=order_id)
    order_item = OrderItem.objects.filter(order=order, product_id=product_id).first()

    if order_item:
        order_item.order_status = "Cancelled"
        order_item.save()

    return redirect("my_orders")


def get_cart_item_count(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.get_or_create(user=user)[0]
        item_count = CartItems.objects.filter(cart=cart).count()
    else:
        item_count = 0

    return JsonResponse({"item_count": item_count})


def coupons_details(request):
    user = request.user
    print(user, "tttt")
    cart = get_object_or_404(Cart, user=user)
    print(cart, "iiii")
    coupons = Coupon.objects.all()
    print(coupons, "qqqqq")

    context = {
        "coupons": coupons,
    }

    return render(request, "usertemplate/coupon_detail.html", context)


def remove_coupon(request):
    user = request.user

    try:
        cart = get_object_or_404(Cart, user=user)
        if cart.coupon:
            cart.coupon = None
            cart.save()
            messages.success(request, "Coupon removed successfully")
        else:
            messages.warning(request, "No coupon applied to your cart")
    except:
        messages.warning(request, "Error: Could not remove coupon")

    return redirect("cart")


def hello(request):
    print("hello")
    arg = request.POST["item"]
    print(arg)
    return JsonResponse({"success": True})
