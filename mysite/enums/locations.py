from django.utils.translation import ugettext_lazy as _

UNALLOCATED = 'U'
ALLOCATED = 'A'
RESERVED = 'R'


def plot_allocation_status():
    allocation_status = [
        (UNALLOCATED, _('Unallocated')),
        (ALLOCATED, _('Allocated')),
        (RESERVED, _('Reserved'))
    ]
    return allocation_status
