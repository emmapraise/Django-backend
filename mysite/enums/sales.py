from django.utils.translation import ugettext_lazy as _

# base status value
PENDING = 0
PAYING = 1
PAID = 2
DISAPPROVED = 3

# withdrawal specific values
COMPLETED = 4

# user payments specific values
VERIFIED = 2
REMITTED = 3

# transaction type values
OUTRIGHT = 'Outright'
INSTALLMENTAL = 'Installmental'


def sale_types():
    types = [
        (OUTRIGHT, _('Outright')),
        (INSTALLMENTAL, _('Installmental'))
    ]

    return types


def sale_status():
    status = [
        (PENDING, _('Pending')),
        (PAYING, _('Paying')),
        (PAID, _('Paid')),
        (REMITTED, _('Remitted(for doc and dev fees)'))
    ]
    return status


def installment_status():
    status = [
        (PENDING, _('Pending')),
        (PAYING, _('Paying')),
        (COMPLETED, _('Completed')),
        (DISAPPROVED, _('Disapproved'))
    ]
    return status
