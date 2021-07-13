from django.utils.translation import ugettext_lazy as _

# base status value
PENDING = 0
PAID = 1
APPROVED = 2
DISAPPROVED = 3

# withdrawal specific values
COMPLETED = 4

# user payments specific values
VERIFIED = 2
REMITTED = 3

# transaction type values
CREDIT = 'CR'
DEBIT = 'DT'


def transaction_types():
    types = [
        (CREDIT, _('Credit')),
        (DEBIT, _('Debit'))
    ]

    return types


def sale_status():
    status = [
        (PENDING, _('Pending')),
        (APPROVED, _('Approved')),
        (PAID, _('Paid')),
        (REMITTED, _('Remitted(for doc and dev fees)'))
    ]
    return status


def installment_status():
    status = [
        (PENDING, _('Pending')),
        (APPROVED, _('Approved')),
        (COMPLETED, _('Completed')),
        (DISAPPROVED, _('Disapproved'))
    ]
    return status
