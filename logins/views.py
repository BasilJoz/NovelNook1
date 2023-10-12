from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib import messages
from .models import user_details
from django.contrib import auth
from . import verify
from admins.models import books, Category
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from userside.models import Review,OrderItem,Order,books
from django.views.decorators.cache import never_cache 


# Create your views here.
@never_cache
def home(request):
    print(request.user, "newone")
    if request.user.is_anonymous:
        
        return redirect('login')
    elif request.user.is_superuser:
        auth.logout(request)
        return redirect('login')
    else:
        
        categories = Category.objects.filter(is_deleted=False)
        
        book = books.objects.filter(deleted=False, categories__is_deleted=False)[:4]

        return render(request, "usertemplate/home.html", {"best_seller": book, "categories": categories})


def handlelogin(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        # print('email','password')
        try:
            user = user_details.objects.get(email=email)
            password_matched = user.check_password(password)
            print(user)
            print(password_matched)
        except:
            messages.error(request, "Invalid email or password")
            return redirect("login")
        if user and password_matched:
            print(1)
            auth.login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid email or password")
            return redirect("login")
    else:
        return render(request, "usertemplate/login.html")


def handlesignup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("number")
        password = request.POST.get("pass1")
        conformpassword = request.POST.get("pass2")
        if password != conformpassword:
            messages.warning(request, "Password is incorrect")
        try:
            if user_details.objects.get(username=username):
                messages.info(request, "username is already taken")
                return redirect("signup")
        except:
            pass

        try:
            if user_details.objects.get(email=email):
                messages.info(request, "email is already taken")
                return redirect("signup")
        except:
            pass

        user = user_details.objects.create(
            username=username, email=email, phone_number=phone
        )
        user.set_password(password)
        user.save()
        auth.login(request, user)
        verify.send(user.phone_number)
        messages.success(request, "Signup sucessfully completed")
        return redirect("Otp", phone, user.id)
    return render(request, "usertemplate/signup.html")


def Otp(request, phone, id):
    user = get_object_or_404(user_details, id=id)

    if request.method == "POST":
        code = request.POST.get("otp")

        if verify.check(phone, code):
            user.is_verified = True
            user.save()
            return redirect("login")
        else:
            user.delete()
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect("signup")
    else:
        return render(request, "usertemplate/otp.html", {"phone": phone, "id": id})


def handleshop(request):
    # Retrieve all categories
    all_categories = Category.objects.filter(is_deleted=False)

    # Retrieve the selected category name from the request's GET parameters
    selected_category_name = request.GET.get("Category")

    # Retrieve the search query from the request's GET parameters
    query = request.GET.get("q")

    # Initialize a queryset to store the filtered books
    filtered_books = books.objects.filter(deleted=False,categories__is_deleted=False)

    # Check if a category was selected and if it exists
    if selected_category_name:
        # Get the category object based on the selected name
        category_instance = get_object_or_404(Category, name=selected_category_name)

        # Filter books by the category object
        filtered_books = filtered_books.filter(categories=category_instance)

    # Check if a search query is provided
    if query:
        # Use Q objects for case-insensitive search on title and author
        filtered_books = filtered_books.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )

    return render(
        request,
        "usertemplate/shop.html",
        {
            "best_seller": filtered_books,
            # "categories": all_categories,
            # "selected_category": selected_category_name,
            # "search_query": query,  # Pass the search query to the template
        },
    )


def Logout(request):
    if user_details.is_authenticated:
        auth.logout(request)
        return redirect("login")


def hanldesingleproduct(request, product_id):
    product = books.objects.get(id=product_id)
    can_write_review = False  # Initialize the flag as False

    # Check if the user is logged in
    if request.user.is_authenticated:
        # Check if the user has ordered this book and it's been delivered
        ordered_book = OrderItem.objects.filter(
            order__user=request.user,
            product=product,
            order_status = 'Delivered'
        )

        if ordered_book:
            can_write_review = True  # Set the flag to True

    # Query the reviews associated with the book
    reviews = Review.objects.filter(book=product)

    context = {
        'book': product,
        'can_write_review': can_write_review,
        'reviews': reviews,  # Pass the reviews to the template
        'products': product
        
    }

    return render(request, 'usertemplate/singlepage.html', context)
    

    



def add_review(request, order_item_id):
    if request.method == 'POST':
        book = get_object_or_404(books, id=order_item_id)
        user = request.user
        rating = request.POST['rating']
        comment = request.POST['comment']

        # Check if the user has ordered and received this book

    Review.objects.create(book=book, user=user, rating=rating, comment=comment)

            # Redirect back to the book detail page or another appropriate page
    return redirect('hanldesingleproduct', product_id=order_item_id)
