from django.utils.translation import ugettext_lazy as _

# gender values
MALE = 'male'
FEMALE = 'female'

# realtor type values
REFERRAL = 'referral'
BUSINESS_PARTNER = 'business partner'
PARTNER = 'partner'
ASSOCIATE_PARTNER = 'associate partner'
EXECUTIVE_PARTNER = 'executive partner'


def gender():
    gender_values = [
        (MALE, _('Male')),
        (FEMALE, _('Female'))
    ]

    return gender_values


def realtor_types():
    realtor_type_values = [
        (REFERRAL, 'Referral'),
        (BUSINESS_PARTNER, 'Business Partner'),
        (PARTNER, 'Partner'),
        (ASSOCIATE_PARTNER, 'Associate Partner'),
        (EXECUTIVE_PARTNER, 'Executive Partner')
    ]
    return realtor_type_values
