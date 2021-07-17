from datetime import date

from dateutil.relativedelta import relativedelta
from django.db.models import Sum

from webapp.models import Payment, Sale, SaleInstallmentPayment, \
    SaleOutrightPayment, Plot, Realtor


def create_sale(client, product, reference):
    payment = Payment.objects.create(client=client, status=Payment.PENDING,
                                     amount=product.installment_amount,
                                     reference=reference)
    if product.duration > 0:
        total_price = product.installment_amount * product.duration
        next_payment_date = date.today() + relativedelta(months=+1)
        sale = Sale.objects.create(client=client, product=product,
                                   total_price=total_price,
                                   gross_price=total_price,
                                   installments=product.duration,
                                   next_payment_date=next_payment_date)
        SaleInstallmentPayment.objects.create(sale=sale, payment=payment,
                                              month=date.today().month,
                                              year=date.today().year)
    else:
        sale = Sale.objects.create(client=client, product=product,
                                   total_price=product.installment_amount,
                                   gross_price=product.installment_amount,
                                   installments=1, next_payment_date=None)
        SaleOutrightPayment.objects.create(payment=payment, sale=sale)
    plot = Plot.objects.filter(location=product.location,
                               plot_type=product.plot_type,
                               status=Plot.UNALLOCATED).first()
    plot.client = client
    plot.status = Plot.RESERVED
    plot.save()
    product.available_units = product.available_units - 1
    product.save()


def check_down_lines(down_line, current_user):
    i = 0
    if Realtor.objects.filter(downline__isnull=True):
        if Realtor.objects.filter(client=down_line).exists():
            referral_sales = Sale.objects.filter(client=down_line).aggregate(
                Sum('gross_price'))
            referral_downlines = Realtor.objects.filter(
                downline=down_line).count()
            print(referral_downlines)
            return referral_sales, referral_downlines
        else:
            pass
    else:
        down_lines = Realtor.objects.filter(id=current_user.id).values_list(
            'downline')
        return check_down_lines(down_lines[i + 1], current_user)
