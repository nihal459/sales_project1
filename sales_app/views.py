from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import *
from django.db import IntegrityError

from django.contrib import messages

from django.contrib.auth import authenticate, login

def sales_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('index')  
        else:
            messages.error(request, "Invalid credentials")
    
    return render(request, 'sales_login.html')


from django.contrib.auth import logout

def sales_logout(request):
    logout(request)
    return redirect('sales_login') 


# Create your views here.
# def index(request):
#     # Calculate total revenue (sum of total_price) and total number of sales
#     total_revenue = Checkout.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
#     total_sales = Checkout.objects.count()  # Count the total number of checkout entries
    
#     # Get the current month and year
#     from datetime import datetime
#     current_month = datetime.now().strftime('%B')  # e.g., 'February'
#     current_year = datetime.now().year

#     # Pass the data to the template
#     context = {
#         'total_revenue': total_revenue,
#         'total_sales': total_sales,
#         'month': current_month,
#         'year': current_year,
#     }

#     return render(request, 'index.html', context)



# def index(request):
#     # Calculate total revenue (sum of total_price) and total number of sales
#     total_revenue = Checkout.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
#     total_sales = Checkout.objects.count()  # Count the total number of checkout entries
    
#     # Get the current month and year
#     from datetime import datetime
#     current_month = datetime.now().strftime('%B')  # e.g., 'February'
#     current_year = datetime.now().year

#     # Get the top 5 selling products
#     top_selling_products = OrderedProduct.objects.values('product__product_name') \
#         .annotate(total_quantity_sold=Sum('product_quantity')) \
#         .order_by('-total_quantity_sold')[:5]  # Get top 5 products by quantity sold
    
#     # Pass the data to the template
#     context = {
#         'total_revenue': total_revenue,
#         'total_sales': total_sales,
#         'month': current_month,
#         'year': current_year,
#         'top_selling_products': top_selling_products,
#     }

#     return render(request, 'index.html', context)



# def index(request):
#     # Calculate total revenue (sum of total_price) and total number of sales
#     total_revenue = Checkout.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
#     total_sales = Checkout.objects.count()  # Count the total number of checkout entries
    
#     # Get the current month and year
#     current_month = datetime.now().strftime('%B')  # e.g., 'February'
#     current_year = datetime.now().year

#     # Get the top 5 selling products
#     top_selling_products = OrderedProduct.objects.values('product__product_name') \
#         .annotate(total_quantity_sold=Sum('product_quantity')) \
#         .order_by('-total_quantity_sold')[:5]  # Get top 5 products by quantity sold

#     # Fetch low stock products (quantity <= 5)
#     low_stock_products = Inventory.objects.filter(quantity__lte=5)  # Low stock filter
    
#     # Pass the data to the template
#     context = {
#         'total_revenue': total_revenue,
#         'total_sales': total_sales,
#         'month': current_month,
#         'year': current_year,
#         'top_selling_products': top_selling_products,
#         'low_stock_products': low_stock_products,  # Pass low stock products
#     }

#     return render(request, 'index.html', context)

from django.db.models import Sum

def index(request):
    # Calculate total revenue (sum of total_price) and total number of sales
    total_revenue = Checkout.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
    total_sales = Checkout.objects.count()  # Count the total number of checkout entries
    
    # Get the current month and year
    from datetime import datetime
    current_month = datetime.now().strftime('%B')  # e.g., 'February'
    current_year = datetime.now().year

    # Get the top 5 selling products
    top_selling_products = OrderedProduct.objects.values('product__product_name') \
        .annotate(total_quantity_sold=Sum('product_quantity')) \
        .order_by('-total_quantity_sold')[:5]  # Get top 5 products by quantity sold

    # Fetch low stock products (quantity <= 5)
    low_stock_products = Inventory.objects.filter(quantity__lte=5)  # Low stock filter

    # Revenue Breakdown by Salesperson
    revenue_by_salesperson = Checkout.objects.values('salesman') \
        .annotate(total_revenue=Sum('total_price')) \
        .order_by('-total_revenue')  # Aggregate revenue per salesperson

    # Pass the data to the template
    context = {
        'total_revenue': total_revenue,
        'total_sales': total_sales,
        'month': current_month,
        'year': current_year,
        'top_selling_products': top_selling_products,
        'low_stock_products': low_stock_products,  # Pass low stock products
        'revenue_by_salesperson': revenue_by_salesperson,  # Pass revenue breakdown
    }

    return render(request, 'index.html', context)



from django.utils.timezone import now
from django.db.models import Sum
import calendar
from datetime import datetime, timedelta



# def get_sales_data(request):
#     # Get current and previous month
#     today = datetime.today()
#     current_month = today.month
#     previous_month = (today - timedelta(days=today.day)).month

#     # Get sales for current and previous months
#     sales_data = (
#         Checkout.objects.filter(payment_status=True, checkout_date__month__in=[current_month, previous_month])
#         .values('checkout_date__month')
#         .annotate(total_sales=Sum('total_price'))
#         .order_by('checkout_date__month')
#     )

#     # Formatting the response
#     formatted_data = {entry['checkout_date__month']: float(entry['total_sales']) for entry in sales_data}

#     return JsonResponse(formatted_data)



def get_sales_data(request):
    # Get current and previous month
    today = datetime.today()
    current_month = today.month
    previous_month = (today - timedelta(days=today.day)).month
    
    # Check the selected time range (daily or weekly)
    time_range = request.GET.get('time_range', 'daily')  # Default to daily

    # Function to get sales data for a given month and time range
    def get_sales_for_month(month):
        start_date = datetime(today.year, month, 1)
        if month == current_month:
            end_date = today
        else:
            end_date = datetime(today.year, month + 1, 1) if month != 12 else datetime(today.year + 1, 1, 1)
        
        # Get sales for the specified month and time range
        if time_range == 'weekly':
            sales_data = (
                Checkout.objects.filter(payment_status=True, checkout_date__gte=start_date, checkout_date__lt=end_date)
                .extra(select={'week': "EXTRACT(week FROM checkout_date)"})
                .values('week')
                .annotate(total_sales=Sum('total_price'))
                .order_by('week')
            )
            # Map weeks to 'Week 1', 'Week 2', etc.
            categories = [f"Week {entry['week']}" for entry in sales_data]
        else:
            # Daily sales data
            sales_data = (
                Checkout.objects.filter(payment_status=True, checkout_date__gte=start_date, checkout_date__lt=end_date)
                .values('checkout_date__day')
                .annotate(total_sales=Sum('total_price'))
                .order_by('checkout_date__day')
            )
            categories = [entry['checkout_date__day'] for entry in sales_data]
        
        # Format the sales data
        sales = [float(entry['total_sales']) for entry in sales_data]
        return categories, sales

    # Get sales data for current and previous months
    current_month_categories, current_month_sales = get_sales_for_month(current_month)
    previous_month_categories, previous_month_sales = get_sales_for_month(previous_month)
    
    # Return data in the format that the frontend expects
    formatted_data = {
        "current_month": {"categories": current_month_categories, "sales": current_month_sales},
        "previous_month": {"categories": previous_month_categories, "sales": previous_month_sales}
    }

    return JsonResponse(formatted_data)




def manage_category(request):
    categories = Category.objects.all()

    if request.method == "POST":
        category_name = request.POST.get('category_name')
        if category_name:
            Category.objects.create(name=category_name)
            return redirect('manage_category')

    return render(request, 'manage_category.html', {'categories': categories})



def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == "POST":
        new_name = request.POST.get('category_name')

        # Check if the new name is different and already exists
        if new_name != category.name and Category.objects.filter(name=new_name).exists():
            return JsonResponse({'error': 'This category already exists'}, status=400)

        try:
            category.name = new_name
            category.save()
            return JsonResponse({'success': 'Category updated successfully'})
        except IntegrityError:
            return JsonResponse({'error': 'This category already exists'}, status=400)

    return JsonResponse({'name': category.name})


def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('manage_category')



def manage_units(request):
    if request.method == "POST":
        unit_name = request.POST.get('unit_name')

        if Unit.objects.filter(unit_type=unit_name).exists():
            return JsonResponse({'error': "This unit already exists"}, status=400)

        Unit.objects.create(unit_type=unit_name)
        return JsonResponse({'success': "Unit added successfully"})

    units = Unit.objects.all()
    return render(request, 'manage_units.html', {'units': units})

def edit_unit(request, unit_id):
    unit = get_object_or_404(Unit, id=unit_id)

    if request.method == "POST":
        new_name = request.POST.get('unit_name')

        if Unit.objects.exclude(id=unit_id).filter(unit_type=new_name).exists():
            return JsonResponse({'error': "This unit already exists"}, status=400)

        unit.unit_type = new_name
        unit.save()
        return JsonResponse({'success': "Unit updated successfully"})

    return JsonResponse({'unit_type': unit.unit_type})

def delete_unit(request, unit_id):
    unit = get_object_or_404(Unit, id=unit_id)
    unit.delete()
    return redirect('manage_units')





def manage_products(request):
    query = request.GET.get("q", "")
    if query:
        materials = Inventory.objects.filter(product_name__icontains=query)
    else:
        materials = Inventory.objects.all()
    
    categories = Category.objects.all()
    units = Unit.objects.all()

    for material in materials:
        material.total_price = material.quantity * material.price_per_unit  # Calculate dynamically


    return render(request, "manage_products.html", {
        "materials": materials,
        "categories": categories,
        "units": units
    })

def add_material(request):
    if request.method == "POST":
        product_name = request.POST.get("product_name")
        category_id = request.POST.get("product_category")
        unit_id = request.POST.get("unit")
        quantity = request.POST.get("quantity")
        price_per_unit = request.POST.get("price_per_unit")

        category = get_object_or_404(Category, id=category_id)
        unit = get_object_or_404(Unit, id=unit_id)

        Inventory.objects.create(
            product_name=product_name,
            product_category=category,
            unit=unit,
            quantity=quantity,
            price_per_unit=price_per_unit
        )

        return redirect("manage_products")

def edit_material(request, pk):
    material = get_object_or_404(Inventory, pk=pk)

    if request.method == "POST":
        material.product_name = request.POST.get("product_name")
        category_id = request.POST.get("product_category")
        unit_id = request.POST.get("unit")
        material.quantity = request.POST.get("quantity")
        material.price_per_unit = request.POST.get("price_per_unit")

        material.product_category = get_object_or_404(Category, id=category_id)
        material.unit = get_object_or_404(Unit, id=unit_id)

        material.save()
        return redirect("manage_products")

def delete_material(request, pk):
    material = get_object_or_404(Inventory, pk=pk)
    material.delete()
    return redirect("manage_products")








def manage_salesman(request):
    salesmen = Salesman.objects.all()
    return render(request, 'manage_salesman.html', {'salesmen': salesmen})


def add_salesman(request):
    if request.method == 'POST':
        name = request.POST.get('salesman_name')
        email = request.POST.get('salesman_email')
        phone_number = request.POST.get('salesman_phone')
        date_of_join = request.POST.get('date_of_join')

        if Salesman.objects.filter(email=email).exists() or Salesman.objects.filter(phone_number=phone_number).exists():
            return JsonResponse({'error': 'Salesman with this email or phone number already exists'})

        Salesman.objects.create(name=name, email=email, phone_number=phone_number, date_of_join=date_of_join)
        return JsonResponse({'success': 'Salesman added successfully'})

    return redirect("manage_salesman")


def edit_salesman(request, salesman_id):
    sales = get_object_or_404(Salesman, id=salesman_id)

    if request.method == "POST":
        new_name = request.POST.get('salesman_name')
        new_email = request.POST.get('salesman_email')
        new_phone = request.POST.get('salesman_phone')
        new_join = request.POST.get('date_of_join')

        # Check if the new name is different and already exists
        if new_name != sales.name and Salesman.objects.filter(name=new_name).exists():
            return JsonResponse({'error': 'This salesman already exists'}, status=400)

        if new_email != sales.email and Salesman.objects.filter(email=new_email).exists():
            return JsonResponse({'error': 'This salesman already exists'}, status=400)

        if new_phone != sales.phone_number and Salesman.objects.filter(phone_number=new_phone).exists():
            return JsonResponse({'error': 'This salesman already exists'}, status=400)


        try:
            sales.name = new_name
            sales.email = new_email
            sales.phone_number = new_phone
            sales.date_of_join = new_join

            sales.save()
            return JsonResponse({'success': 'Salesman updated successfully'})
        except IntegrityError:
            return JsonResponse({'error': 'This salesman already exists'}, status=400)

    return JsonResponse({'name': sales.name})





def delete_salesman(request, salesman_id):
    salesman = get_object_or_404(Salesman, id=salesman_id)
    salesman.delete()
    messages.success(request, 'Salesman deleted successfully')
    return redirect('manage_salesman') 


def invoice(request):
    cart_items = AddToCart.objects.all()
    return render(request, "invoice.html", {"cart_items": cart_items})

def search_products(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Ensure AJAX request
        query = request.GET.get('term', '').strip()
        products = Inventory.objects.filter(product_name__icontains=query)[:10]
        product_list = [{"label": p.product_name, "value": p.product_name} for p in products]
        return JsonResponse(product_list, safe=False)
    return JsonResponse([], safe=False)

# Fetch salesmen matching the query
def search_salesmen(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Ensure AJAX request
        query = request.GET.get('term', '').strip()
        salesmen = Salesman.objects.filter(name__icontains=query)[:10]
        salesman_list = [{"label": s.name, "value": s.name} for s in salesmen]
        return JsonResponse(salesman_list, safe=False)
    return JsonResponse([], safe=False)


def add_to_cart(request):
    if request.method == "POST":
        product_name = request.POST.get("product_name", "").strip()

        # Check if input is empty
        if not product_name:
            messages.error(request, "Nothing to add")
            return redirect("invoice")  # Redirect to invoice.html

        try:
            product = Inventory.objects.get(product_name__iexact=product_name)  # Case-insensitive lookup

            # Check if product already in cart
            cart_item, created = AddToCart.objects.get_or_create(product=product)

            if not created:
                cart_item.product_quantity += 1  # Increase quantity
            cart_item.price = cart_item.product_quantity * product.price_per_unit  # Update total price
            cart_item.save()

            messages.success(request, f"{product_name} added to cart ({cart_item.product_quantity})")
        except Inventory.DoesNotExist:
            messages.error(request, "Invalid product, not present in inventory")
    
    return redirect("invoice") 


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import AddToCart
import json

@csrf_exempt
def update_cart_item(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = data.get('quantity')
        price = data.get('price')

        try:
            cart_item = AddToCart.objects.get(id=item_id)
            cart_item.product_quantity = quantity
            cart_item.price = price
            cart_item.save()

            return JsonResponse({'success': True, 'updated_price': price})
        except AddToCart.DoesNotExist:
            return JsonResponse({'success': False})

@csrf_exempt
def remove_from_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data.get('item_id')

        try:
            cart_item = AddToCart.objects.get(id=item_id)
            cart_item.delete()
            return JsonResponse({'success': True})
        except AddToCart.DoesNotExist:
            return JsonResponse({'success': False})


########################################################################################################################################
########################################################################################################################################
########################################################################################################################################
        
from decimal import Decimal

# def save_invoice(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
            
#             customer_name = data.get('customer_name', '')
#             phone_number = data.get('customer_phone', '')
#             salesman_name = data.get('salesman_name', '')
#             discount = Decimal(data.get('discount', 0))  # Convert to Decimal
#             amount_received = Decimal(data.get('amount_received', 0))  # Convert to Decimal
            
#             cart_items = AddToCart.objects.all()  # Fetch all cart items
            
#             if not cart_items.exists():
#                 return JsonResponse({'success': False, 'message': 'Cart is empty'})

#             # Calculate total price before discount (Ensure consistent Decimal usage)
#             total_price = sum(Decimal(item.price) for item in cart_items) - discount
            
#             # Save Checkout
#             checkout = Checkout.objects.create(
#                 customer_name=customer_name,
#                 phone_number=phone_number,
#                 salesman=salesman_name,
#                 total_price=total_price,
#                 amount_received=amount_received
#             )
            
#             # Save Ordered Products
#             for item in cart_items:
#                 OrderedProduct.objects.create(
#                     checkout=checkout,
#                     product=item.product,
#                     product_quantity=item.product_quantity,
#                     product_price=item.price
#                 )

#             # Clear the cart after checkout
#             cart_items.delete()

#             return JsonResponse({'success': True, 'message': 'Invoice saved successfully'})
#         except Exception as e:
#             return JsonResponse({'success': False, 'message': str(e)})

#     return JsonResponse({'success': False, 'message': 'Invalid request method'})




def save_invoice(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            customer_name = data.get('customer_name', '')
            phone_number = data.get('customer_phone', '')
            salesman_name = data.get('salesman_name', '')
            discount = Decimal(data.get('discount', 0))
            amount_received = Decimal(data.get('amount_received', 0))
            
            cart_items = AddToCart.objects.all()  # Fetch all cart items
            
            if not cart_items.exists():
                return JsonResponse({'success': False, 'message': 'Cart is empty'})

            # Validate stock availability
            insufficient_stock = []
            for item in cart_items:
                inventory_item = Inventory.objects.get(id=item.product.id)
                if item.product_quantity > inventory_item.quantity:
                    insufficient_stock.append(f"{inventory_item.product_name} has only {inventory_item.quantity} left")

            if insufficient_stock:
                return JsonResponse({'success': False, 'message': ', '.join(insufficient_stock)})

            # Calculate total price before discount
            total_price = sum(Decimal(item.price) for item in cart_items) - discount

            # Save Checkout
            checkout = Checkout.objects.create(
                customer_name=customer_name,
                phone_number=phone_number,
                salesman=salesman_name,
                total_price=total_price,
                amount_received=amount_received
            )

            # Save Ordered Products & Deduct from Inventory
            for item in cart_items:
                inventory_item = Inventory.objects.get(id=item.product.id)
                
                # Deduct ordered quantity from stock
                inventory_item.quantity -= item.product_quantity
                inventory_item.save()

                # Create ordered product entry
                OrderedProduct.objects.create(
                    checkout=checkout,
                    product=item.product,
                    product_quantity=item.product_quantity,
                    product_price=item.price
                )

            # Clear the cart after checkout
            cart_items.delete()

            return JsonResponse({'success': True, 'message': 'Invoice saved successfully'})
        
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})



from django.db.models import Q

def manage_invoices(request):
    query = request.GET.get("q", "")
    invoices = Checkout.objects.all()

    if query:
        invoices = Checkout.filter(
            Q(customer_name__icontains=query) |
            Q(salesman__icontains=query) |
            Q(total_price__icontains=query)
        )

    context = {
        "invoices": invoices
    }
    return render(request, "manage_invoices.html", context)




def invoice_details(request, invoice_id):
    invoice = get_object_or_404(Checkout, id=invoice_id)
    ordered_products = invoice.ordered_products.all()  # Fetch products related to this invoice
    
    context = {
        "invoice": invoice,
        "ordered_products": ordered_products
    }
    return render(request, "invoice_details.html", context)




# def edit_invoice(request, invoice_id):
#     invoice = get_object_or_404(Checkout, id=invoice_id)
#     ordered_products = invoice.ordered_products.all()
#     salesman = Salesman.objects.all()

#     if request.method == "POST":
#         invoice.customer_name = request.POST.get("customer_name")
#         invoice.phone_number = request.POST.get("phone_number")
#         invoice.salesman = request.POST.get("salesman")
#         invoice.amount_received = Decimal(request.POST.get("amount_received"))

#         # Update ordered products
#         for product in ordered_products:
#             quantity_field = f"quantity_{product.id}"
#             if quantity_field in request.POST:
#                 new_quantity = int(request.POST.get(quantity_field))
#                 product.product_quantity = new_quantity
#                 product.product_price = product.product.price_per_unit * new_quantity
#                 product.save()

#         # Recalculate total price and amount remaining
#         invoice.total_price = sum(p.product_price for p in ordered_products)
#         invoice.amount_remaining = invoice.total_price - invoice.amount_received
#         invoice.payment_status = invoice.amount_remaining == 0

#         invoice.save()
#         return redirect("invoice_details", invoice_id=invoice.id)

#     context = {
#         "invoice": invoice,
#         "ordered_products": ordered_products,
#         'salesman':salesman,
#     }
#     return render(request, "edit_invoice.html", context)

def edit_invoice(request, invoice_id):
    invoice = get_object_or_404(Checkout, id=invoice_id)
    ordered_products = invoice.ordered_products.all()
    salesman = Salesman.objects.all()

    if request.method == "POST":
        invoice.customer_name = request.POST.get("customer_name")
        invoice.phone_number = request.POST.get("phone_number")
        invoice.salesman = request.POST.get("salesman")
        invoice.amount_received = Decimal(request.POST.get("amount_received"))

        # Update ordered products
        for product in ordered_products:
            quantity_field = f"quantity_{product.id}"
            if quantity_field in request.POST:
                new_quantity = request.POST.get(quantity_field)
                try:
                    # Convert the quantity to float first, then to int (if needed)
                    new_quantity = float(new_quantity)  # Convert to float first
                    new_quantity = int(new_quantity)    # Convert to int
                except ValueError:
                    new_quantity = 0  # Default to 0 if invalid

                product.product_quantity = new_quantity
                product.product_price = product.product.price_per_unit * new_quantity
                product.save()

        # Recalculate total price and amount remaining
        invoice.total_price = sum(p.product_price for p in ordered_products)
        invoice.amount_remaining = invoice.total_price - invoice.amount_received
        invoice.payment_status = invoice.amount_remaining == 0

        invoice.save()
        return redirect("invoice_details", invoice_id=invoice.id)

    context = {
        "invoice": invoice,
        "ordered_products": ordered_products,
        'salesman': salesman,
    }
    return render(request, "edit_invoice.html", context)




def remove_product(request, product_id):
    product = get_object_or_404(OrderedProduct, id=product_id)
    invoice_id = product.checkout.id
    product.delete()
    return redirect("edit_invoice", invoice_id=invoice_id)

def add_product_to_invoice(request, invoice_id):
    invoice = get_object_or_404(Checkout, id=invoice_id)
    if request.method == "POST":
        product_id = request.POST.get("product")
        quantity = int(request.POST.get("quantity"))

        product = get_object_or_404(Inventory, id=product_id)
        product_price = product.price_per_unit * quantity

        OrderedProduct.objects.create(
            checkout=invoice, product=product, product_quantity=quantity, product_price=product_price
        )

        return redirect("edit_invoice", invoice_id=invoice.id)

    available_products = Inventory.objects.all()
    return render(request, "add_product.html", {"invoice": invoice, "available_products": available_products})




def delete_invoice(request, invoice_id):
    invoice = get_object_or_404(Checkout, id=invoice_id)
    
    # Delete all related OrderedProducts
    invoice.ordered_products.all().delete()
    
    # Delete the invoice (Checkout)
    invoice.delete()

    messages.success(request, "Invoice and related records deleted successfully.")
    return redirect('manage_invoices')  # Change 'invoice_list' to your actual invoice listing view name
