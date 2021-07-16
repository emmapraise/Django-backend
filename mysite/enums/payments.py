from django.utils.translation import ugettext_lazy as _

# base status value
PENDING = 0
APPROVED = 1
DISAPPROVED = 2

# withdrawal specific values
DISBURSED = 2

# user payments specific values
VERIFIED = 2
REMITTED = 3

#Payment Type
OUTRIGHT = 'Outright Sale'
INSTALLMENT = 'Installmental Sale'
TOUPUP = 'Topup'

# transaction type values
CREDIT = 'CR'
DEBIT = 'DT'


def transaction_types():
    types = [
        (CREDIT, _('Credit')),
        (DEBIT, _('Debit'))
    ]

    return types

def payment_types():
    types = [
        (OUTRIGHT, _('Outright Sale')),
        (INSTALLMENT, _('Installmental Sale')),
        (TOUPUP, _('Topup'))
    ]

    return types

def payment_status():
    status = [
        (PENDING, _('Pending')),
        (APPROVED, _('Approved')),
        (VERIFIED, _('Verified')),
        (REMITTED, _('Remitted(for doc and dev fees)'))
    ]
    return status


def withdrawal_status():
    status = [
        (PENDING, _('Pending')),
        (APPROVED, _('Approved')),
        (DISBURSED, _('Disbursed')),
        (DISAPPROVED, _('Disapproved'))
    ]
    return status
