from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Transaction.models import FarmInvoice,TradeInvoice

@login_required
def invoices(request):
  if request.user:
    if request.user.is_superuser:
      print('kong')
    else:
      messages.error(request, 'User is not authorized')
      return redirect('farms_page')
  context = {
    'farms' : FarmInvoice.objects.all(),
    'trades' : TradeInvoice.objects.all()
  }
  return render(request, 'invoice.html', context)