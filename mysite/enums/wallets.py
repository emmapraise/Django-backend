from django.utils.translation import ugettext_lazy as _

# base status value
PENDING = 0
PAID = 1
DISAPPROVED = 2

# withdrawal specific values
COMPLETED = 4


# transaction type values
SALE = 'Sale'
TOPUP = 'Topup'
COMMISSION = 'Commission'
WITHDRAWAL = 'Withdrawal'


def wallet_types():
    types = [
        (SALE, _('Sale')),
        (TOPUP, _('Topup')),
        (COMMISSION, _('Commission')),
        (WITHDRAWAL, _('Withdrawal'))
    ]

    return types


def wallet_status():
    status = [
        (PENDING, _('Pending')),
        (PAID, _('Paid')),
    ]
    return status
