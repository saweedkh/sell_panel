# Django Built-in modules
from django.core.management.base import BaseCommand

# Local apps
from gateways import bankfactories, models as bank_models, default_settings as settings


class Command(BaseCommand):
    help = "Reconfirmation request from the bank"

    def handle(self, *args, **kwargs):
        factory = bankfactories.BankFactory()
        bank_models.Bank.objects.update_expire_records()

        for item in bank_models.Bank.objects.filter_return_from_bank():
            bank = factory.create(bank_type=item.bank_type, identifier=item.bank_choose_identifier)
            bank.verify(item.tracking_code)
