from django.shortcuts import render, redirect 
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
import json
# generate email
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string, get_template

import qrcode

from .forms import *
from .filters import *

# === for all staff and customers ===

# make orders
def index(request):
    categories = Category.objects.filter(active=True).all()

    return render(request, 'main/index.html', {
        'categories': categories,
    })

def checkout(request):
    
    products = Product.objects.filter(active=True).all()
    if request.method == 'POST':
        # set all total to 0
        total_hot_items = 0
        total_cold_items = 0
        amount_hot = 0
        amount_cold = 0

        for product in products:

            # display what are the customers ordering

            if len(request.POST.get(f'{product.id} hot')) < 1:
                product.data_hot = 0
            else:
                product.data_hot = int(request.POST.get(f'{product.id} hot'))
                # subtotal for product
                product.subtotal = product.price * product.data_hot
                # count total
                total_hot_items += product.data_hot
                amount_hot += product.subtotal
            
            if len(request.POST.get(f'{product.id} cold')) < 1:
                product.data_cold = 0
            else:
                product.data_cold = int(request.POST.get(f'{product.id} cold'))
                # subtotal for product
                product.subtotal = product.price * product.data_cold
                # count total
                total_cold_items += product.data_cold
                amount_cold += product.subtotal
        
        total_items = total_hot_items + total_cold_items
        amount = amount_hot+ amount_cold
        
        return render(request, 'main/checkout.html', {
            'products': products,
            'total_items': total_items,
            'amount': amount,
            'orderForm': OrderForm(),
            'staffOrderForm': StaffOrderForm()
        })

def confirm(request):
    products = Product.objects.filter(active=True).all()

    if request.method == 'POST':
        store = request.POST.get("store")
        stay = request.POST.get("stay")
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")

        # save customer and order
        if email == None: # customers order with staff won't save to database
            # save order
            order = Order(
                store = store,
                stay = stay,
                status = 'Pending'
            )
            order.save()
        else:
            # check if customer has shopped once
            customer, created = Customer.objects.get_or_create(email=email)

            customer.name = name
            customer.phone = phone
            customer.save()

            # save order
            order = Order(
                customer = customer,
                store = store,
                stay = stay,
                status = 'Pending',
            )
            order.save()

        # save orderItem   
        for product in products:
            if request.POST.get(f'{product.id} hot') == None:
                pass # ignore empty value
            else:
                product.data_hot = request.POST.get(f'{product.id} hot')
                hot = OrderItem(
                    order = order,
                    product = product,
                    hotOrCold = 'Hot',
                    qty = product.data_hot
                )
                hot.save()
            if request.POST.get(f'{product.id} cold') == None:
                pass # ignore empty value
            else:
                product.data_cold = request.POST.get(f'{product.id} cold')
                cold = OrderItem(
                    order = order,
                    product = product,
                    hotOrCold = 'Cold',
                    qty = product.data_cold
                )
                cold.save()

        # send email
        if email != None:
            template = get_template('main/email.html').render({
                'order': order,
            })
            emailmsg = EmailMessage(
                'Order Confirmaion from TEA Time', # subject
                template, # body
                settings.EMAIL_HOST_USER, # sender
                [email], # reciever
            )
            emailmsg.content_subtype = 'html'
            emailmsg.fail_silently = False
            emailmsg.send()
        
    return render(request, 'main/confirm.html', {
        'store': store,
        'stay': stay,
        'phone': phone,
        'email': email,
        'order': order,
    })


# === for staff only ===

def login_view(request):
    if request.method == 'POST':

        # attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "staff/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "staff/login.html")

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_staff)
def manage_products(request):
    all_products = Product.objects.all().order_by('code')

    # filter for products
    filter = ProductFilter(request.GET, queryset=all_products)
    all_products = filter.qs

    return render(request, "staff/manage_products.html", {
        'all_products': all_products,
        'filter': filter,
    })

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_staff)
def new_product(request):

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            code = form.cleaned_data['code']           
            price = form.cleaned_data['price']
            category = form.cleaned_data['category']
            hot = form.cleaned_data['hot']
            cold = form.cleaned_data['cold']

            new = Product(
                name = name,
                code = code,
                price = price,
                category = category,
                hot = hot,
                cold = cold,
            )
            new.save()
            
            return HttpResponseRedirect(f"../manage_products")

    else: 
        return render(request, "staff/new_product.html", {
            'form': ProductForm(),
        })


@login_required(login_url='login')
@user_passes_test(lambda u: u.is_staff)
def edit_product(request, pk):
    try:
        product = Product.objects.get(id=pk)
        form = ProductForm(instance=product)

        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(f"../manage_products")

        else: 
            return render(request, "staff/edit_product.html", {
                'form': form,
            })

    except Product.DoesNotExist:
        raise Http404("Oops! Product not found.")

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_staff)
def category(request):
    categories = Category.objects.all().order_by('name')
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            image = form.cleaned_data['image']

            new = Category(
                name = name,
                image = image,
            )
            new.save()
            return HttpResponseRedirect(reverse('category'))

    return render(request, "staff/category.html", {
        'categories': categories,
        'form': form,
    })

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_staff)
def edit_category(request, pk):
    try:
        category = Category.objects.get(id=pk)
        form = CategoryForm(instance=category)

        if request.method == 'POST':
            form = CategoryForm(request.POST, request.FILES, instance=category)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('category'))

        else: 
            return render(request, "staff/edit_category.html", {
                'form': form,
            })

    except Product.DoesNotExist:
        raise Http404("Oops! Product not found.")


@login_required(login_url='login')
@user_passes_test(lambda u: u.is_staff)
def manage_orders(request):
    orders = Order.objects.all().order_by('status', 'id')

    # filter for products
    filter = OrderFilter(request.GET, queryset=orders)
    orders = filter.qs

    change_status = False
    for order in orders:
        if order.status == 'Pending':
            change_status = True

    return render(request, 'staff/manage_orders.html', {
        'orders': orders,
        'filter': filter,
        'change_status': change_status,
    })

def cancel(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    order = Order.objects.get(id=data['order'])
    order.status = 'Cancelled'
    order.save()
    return HttpResponse(status=204)

def delivered(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    order = Order.objects.get(id=data['order'])
    order.status = 'Delivered'
    order.save()
    return HttpResponse(status=204)


@login_required(login_url='login')
@user_passes_test(lambda u: u.is_staff)
def report(request):
    orders = Order.objects.exclude(status='Cancelled').order_by('-id')

    # filter for items
    filter = ReportFilter(request.GET, queryset=orders)
    orders = filter.qs

    sales_qty = 0
    sales_amount = 0
    for order in orders:
        for item in order.get_items:
            sales_qty += item.qty
            sales_amount += item.get_subtotal
    
    return render(request, 'staff/report.html', {
        'orders': orders,
        'filter': filter,
        'sales_qty': sales_qty,
        'sales_amount': sales_amount,
    })

