from django.apps import AppConfig


class MyapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapi'

    def ready(self):
        print('starting scheduler...')
        from .payment_schedule import installment
        installment.start()
