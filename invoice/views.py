from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from .models import OnlyPInv, OnlyBInv,OnlyPCn,OnlyBCn,OnlyPDn,OnlyBDn,CustomUser,Trader
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404


# 1. Show all unique GSTINs from both tables
#@login_required
#def gstin_list(request):
#    gstins_p = OnlyPInv.objects.values_list('my_gstin', flat=True).distinct()
#    gstins_b = OnlyBInv.objects.values_list('my_gstin', flat=True).distinct()
#    gstins_pc = OnlyPCn.objects.values_list('my_gstin', flat=True).distinct()
#    gstins_bc = OnlyBCn.objects.values_list('my_gstin', flat=True).distinct()
#    gstins_pd = OnlyPDn.objects.values_list('my_gstin', flat=True).distinct()
#    gstins_bd = OnlyBDn.objects.values_list('my_gstin', flat=True).distinct()
#    gstins = sorted(set(gstins_p) | set(gstins_b) | set(gstins_pc) | set(gstins_bc) | set(gstins_pd) | set(gstins_bd))  # Merge and sort
#    return render(request, 'gstin_list.html', {'gstins': gstins})

# views.py

@never_cache
@login_required
# views.py

def gstin_list(request):
    user_mobile = request.user.mobile

    # Get unique trader entries based on mobile number
    traders = Trader.objects.filter(mo=user_mobile).values('trader_name', 'gstin').distinct()
    cp_name = Trader.objects.filter(mo=user_mobile).values_list('contact_person_name', flat=True).first()


    # Convert QuerySet to list of dictionaries (or you can use tuples)
    trader_list = list(traders)

    return render(request, 'gstin_list.html', {'traders': trader_list,'cp_name':cp_name})


# 2. Show both P and B invoice tables for selected GSTIN (single page)
@never_cache
@login_required
@never_cache
@login_required
def gstin_detail(request, gstin):
    user_mobile = request.user.mobile

    # ✅ Check if this GSTIN belongs to the current user
    trader_obj = Trader.objects.filter(mo=user_mobile, gstin=gstin).first()
    if not trader_obj:
        # ❌ If not found, return 403 Forbidden or redirect to a safe page
        return HttpResponse("""
            <html>
            <head><title>Oops!</title></head>
            <body style="font-family: Arial; background-color: #fffbe6; text-align: center; padding-top: 50px;">
                <h1>🚫 Access Denied!</h1>
                <p>Nice try, detective 🕵️‍♂️... but this GSTIN doesn't belong to you!</p>
                <p>Please to go back before the audit police arrive! 👮‍♀️💼</p>
            </body>
            </html>
        """)

    trader = trader_obj.trader_name
    cp_name = trader_obj.contact_person_name

    p_invoices = OnlyPInv.objects.filter(my_gstin=gstin)    
    b_invoices = OnlyBInv.objects.filter(my_gstin=gstin)
    p_credit_notes = OnlyPCn.objects.filter(my_gstin=gstin)
    b_credit_notes = OnlyBCn.objects.filter(my_gstin=gstin)
    p_debit_notes = OnlyPDn.objects.filter(my_gstin=gstin)
    b_debit_notes = OnlyBDn.objects.filter(my_gstin=gstin)

    context = {
        'gstin': gstin,
        'trader' : trader,
        'cp_name': cp_name,
        'p_invoices': p_invoices,
        'b_invoices': b_invoices,
        'p_credit_notes': p_credit_notes,
        'b_credit_notes': b_credit_notes,
        'p_debit_notes': p_debit_notes,
        'b_debit_notes': b_debit_notes,
    }

    return render(request, 'gstin_detail.html', context)



@never_cache
def register_view(request):
    if request.method == 'POST':
        mobile = request.POST['mobile']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if CustomUser.objects.filter(mobile=mobile).exists():
            messages.error(request, "Mobile number already exists.")
            return redirect('register')

        user = CustomUser.objects.create(
            mobile=mobile,
            password=make_password(password)
        )
        user.save()
        messages.success(request, "Registration successful. Please login.")
        return redirect('login')

    return render(request, 'register.html')

@never_cache
def login_view(request):
    if request.method == 'POST':
        mobile = request.POST['mobile']
        password = request.POST['password']
        user = authenticate(request, username=mobile, password=password)

        if user is not None:
            login(request, user)
            return redirect('gstin_list')  # Updated from 'home' to 'dashboard'
        else:
            messages.error(request, "Invalid mobile or password.")

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

def base_view(request):
    return render(request, 'base.html')


def dashboard_view(request):
    return render(request, 'dashboard.html')
    from django.shortcuts import render
from .models import OnlyPInv, OnlyBInv, OnlyPCn, OnlyBCn, OnlyPDn, OnlyBDn

def public_gstin_data(request):
    gstin = request.GET.get("gstin", "").strip()
    tab = request.GET.get("tab", "")
    q = request.GET.get("q", "").strip().lower()
    trader = Trader.objects.filter(gstin=gstin).values('trader_name').first()['trader_name']

    # Initialize all tables as empty
    p_invoices = OnlyPInv.objects.none()
    b_invoices = OnlyBInv.objects.none()
    p_credit_notes = OnlyPCn.objects.none()
    b_credit_notes = OnlyBCn.objects.none()
    p_debit_notes = OnlyPDn.objects.none()
    b_debit_notes = OnlyBDn.objects.none()

    if not gstin:
        context = {
            'error': 'GSTIN not provided.',
            'active_tab': tab,
        }
        return render(request, 'public_table.html', context)

    # Always fetch all data for the GSTIN
    p_invoices_all = OnlyPInv.objects.filter(my_gstin=gstin)
    b_invoices_all = OnlyBInv.objects.filter(my_gstin=gstin)
    p_credit_notes_all = OnlyPCn.objects.filter(my_gstin=gstin)
    b_credit_notes_all = OnlyBCn.objects.filter(my_gstin=gstin)
    p_debit_notes_all = OnlyPDn.objects.filter(my_gstin=gstin)
    b_debit_notes_all = OnlyBDn.objects.filter(my_gstin=gstin)

    # Apply search query to all datasets
    if q:
        p_invoices = p_invoices_all.filter(supplier_trade_name__icontains=q)
        b_invoices = b_invoices_all.filter(supplier_trade_name__icontains=q)
        p_credit_notes = p_credit_notes_all.filter(supplier_trade_name__icontains=q)
        b_credit_notes = b_credit_notes_all.filter(supplier_trade_name__icontains=q)
        p_debit_notes = p_debit_notes_all.filter(supplier_trade_name__icontains=q)
        b_debit_notes = b_debit_notes_all.filter(supplier_trade_name__icontains=q)
    else:
        # No search query? Show all
        p_invoices = p_invoices_all
        b_invoices = b_invoices_all
        p_credit_notes = p_credit_notes_all
        b_credit_notes = b_credit_notes_all
        p_debit_notes = p_debit_notes_all
        b_debit_notes = b_debit_notes_all

    context = {
        'p_invoices': p_invoices,
        'b_invoices': b_invoices,
        'p_credit_notes': p_credit_notes,
        'b_credit_notes': b_credit_notes,
        'p_debit_notes': p_debit_notes,
        'b_debit_notes': b_debit_notes,
        'active_tab': tab,
        'search_query': q,
        'gstin': gstin,
        'trader':trader
    }

    return render(request, 'public_table.html', context)