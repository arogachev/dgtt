from django.core.management.base import BaseCommand
from django.db import transaction

from ...factories import BuildingFactory, CategoryFactory, OrganizationFactory


class Command(BaseCommand):
    BUILDINGS_COUNT = 10000
    CATEGORIES_CHILDREN_PER_LEVEL = (5, 4, 3, 2)
    ORGANIZATIONS_COUNT = 100000

    help = 'Seed database'

    @transaction.atomic
    def handle(self, *args, **options):
        BuildingFactory.create_batch(self.BUILDINGS_COUNT)
        CategoryFactory.create_batch_tree(self.CATEGORIES_CHILDREN_PER_LEVEL)
        OrganizationFactory.create_batch(self.ORGANIZATIONS_COUNT)
