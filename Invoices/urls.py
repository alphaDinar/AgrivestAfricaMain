from django.urls import path
from . import views

urlpatterns = [
    path('invoices/',views.invoices,name='invoice_page'),
]