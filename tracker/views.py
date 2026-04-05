import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from .models import Budget
from .forms import BudgetForm
import datetime

from .models import Transaction, Category
from .forms import TransactionForm


import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Sum

from .models import Transaction


@login_required
def home(request):
    transactions = Transaction.objects.filter(user=request.user)

    # =====================
    # TOTALS (NO transaction_type ❌)
    # =====================
    total_income = (
        transactions
        .filter(category__category_type='Income')
        .aggregate(total=Sum('amount'))['total'] or 0
    )

    total_expense = (
        transactions
        .filter(category__category_type='Expense')
        .aggregate(total=Sum('amount'))['total'] or 0
    )

    balance = total_income - total_expense

    # =====================
    # CATEGORY-WISE EXPENSE (PIE CHART)
    # =====================
    expense_by_category = (
        transactions
        .filter(category__category_type='Expense')
        .values('category__name')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    categories = json.dumps([
        item['category__name'] or 'Uncategorized'
        for item in expense_by_category
    ])

    category_totals = json.dumps([
        float(item['total']) for item in expense_by_category
    ])

    context = {
        'transactions': transactions.order_by('-date'),
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'categories': categories,
        'category_totals': category_totals,
    }

    return render(request, 'dashboard.html', context)



@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('home')
    else:
        form = TransactionForm()

    return render(request, 'add_transaction.html', {'form': form})


@login_required
def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TransactionForm(instance=transaction)

    return render(request, 'add_transaction.html', {
        'form': form,
        'edit_mode': True
    })


@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)

    if request.method == 'POST':
        transaction.delete()
        return redirect('home')

    return render(request, 'confirm_delete.html', {
        'transaction': transaction
    })



@login_required
def add_budget(request):
    today = datetime.date.today()

    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect('home')
    else:
        form = BudgetForm(initial={
            'month': today.month,
            'year': today.year
        })

    return render(request, 'add_budget.html', {
        'form': form
    })



@login_required
def budget_list(request):
    budgets = Budget.objects.filter(user=request.user).order_by('-year', '-month')
    return render(request, 'budget_list.html', {
        'budgets': budgets
    })












"""import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth

from .models import Transaction
from .forms import TransactionForm


@login_required
def home(request):
    transactions = Transaction.objects.filter(user=request.user)

    # =====================
    # TOTALS
    # =====================
    total_income = (
        transactions
        .filter(transaction_type='Income')
        .aggregate(total=Sum('amount'))['total'] or 0
    )

    total_expense = (
        transactions
        .filter(transaction_type='Expense')
        .aggregate(total=Sum('amount'))['total'] or 0
    )

    balance = total_income - total_expense

    # =====================
    # CATEGORY-WISE EXPENSE (FOR CHART)
    # =====================
    expense_by_category = (
        transactions
        .filter(transaction_type='Expense')
        .values('category__name')
        .annotate(total=Sum('amount'))
    )

    # Convert to JSON-safe structures
    categories = json.dumps([
        item['category__name'] for item in expense_by_category
    ])

    category_totals = json.dumps([
        float(item['total']) for item in expense_by_category
    ])

    context = {
        'transactions': transactions.order_by('-date'),
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'categories': categories,
        'category_totals': category_totals,
    }

    return render(request, 'dashboard.html', context)


@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('home')
    else:
        form = TransactionForm()

    return render(request, 'add_transaction.html', {'form': form})



@login_required
def edit_transaction(request, pk):
    transaction = Transaction.objects.get(pk=pk, user=request.user)

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TransactionForm(instance=transaction)

    return render(request, 'add_transaction.html', {
        'form': form,
        'edit_mode': True
    })



@login_required
def delete_transaction(request, pk):
    transaction = Transaction.objects.get(pk=pk, user=request.user)

    if request.method == 'POST':
        transaction.delete()
        return redirect('home')

    return render(request, 'confirm_delete.html', {
        'transaction': transaction
    })
"""