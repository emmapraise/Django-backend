from django.utils.translation import ugettext_lazy as _

# Request status
PENDING = 0
APPROVED = 1
DISAPPROVED = 2
PAID = 3
IMPLEMENTED = 4

# Change request parameters
PRODUCT = 0
PROMOTION = 1
OWNERSHIP = 2
OTHERS = 3


def change_parameters():
    parameters = [
        (PRODUCT, _('Product')),
        (PROMOTION, _('Promotion')),
        (OWNERSHIP, _('Ownership')),
        (OTHERS, _('Others'))
    ]
    return parameters


def request_status():
    status = [
        (PENDING, _('Pending')),
        (APPROVED, _('Approved')),
        (DISAPPROVED, _('Disapproved')),
        (PAID, _('Paid')),
        (IMPLEMENTED, _('Implemented'))
    ]
    return status
