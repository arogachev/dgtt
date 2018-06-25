from functools import reduce
from random import randint

from django.contrib.gis.geos import Point
import factory
from faker.providers import BaseProvider

from .models import Building, Category, Organization

LOCALE = 'ru_RU'


class CoordinatesProvider(BaseProvider):
    CENTER_COORDINATES = (54.873950, 69.152105)
    RADIUS = 5

    def coordinates(self):
        latitude = factory.Faker('geo_coordinate', center=self.CENTER_COORDINATES[0], radius=self.RADIUS).generate({})
        longitude = factory.Faker('geo_coordinate', center=self.CENTER_COORDINATES[1], radius=self.RADIUS).generate({})
        return Point((latitude, longitude))


class CategoryProvider(BaseProvider):
    WORDS_COUNT_MIN = 1
    WORDS_COUNT_MAX = 3

    INSTANCES_COUNT_MIN = 1
    INSTANCES_COUNT_MAX = 3

    def __init__(self, generator):
        super().__init__(generator)
        self._iterator = factory.Iterator(Category.objects.order_by('pk').all())

    def category_name(self):
        words_count = randint(self.WORDS_COUNT_MIN, self.WORDS_COUNT_MAX)
        words = factory.Faker('words', nb=words_count).generate({})
        return ' '.join(words).capitalize()

    def category_instances(self):
        count = randint(self.INSTANCES_COUNT_MIN, self.INSTANCES_COUNT_MAX)
        return tuple(self._iterator.evaluate(None, None, None) for _ in range(count))


class PhonesProvider(BaseProvider):
    COUNT_MIN = 1
    COUNT_MAX = 3

    def phones(self):
        count = randint(self.COUNT_MIN, self.COUNT_MAX)
        return [factory.Faker('phone_number').generate({}) for _ in range(count)]


factory.Faker._DEFAULT_LOCALE = LOCALE
factory.Faker.add_provider(CoordinatesProvider)
factory.Faker.add_provider(CategoryProvider)
factory.Faker.add_provider(PhonesProvider)


class BuildingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Building

    address = factory.Faker('address')
    coordinates = factory.Faker('coordinates')


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker('category_name')

    @classmethod
    def create_batch_tree(cls, children_per_level):
        items_per_level = tuple(
            reduce(lambda x, y: x * y, children_per_level[:level + 1])
            for level, _ in enumerate(children_per_level)
        )
        categories_map = {level: [] for level, _ in enumerate(children_per_level)}
        prev_level_items_count = 0

        for level, items_count in enumerate(items_per_level):
            prev_level = level - 1

            for item_number in range(items_count):
                category = CategoryFactory.build()

                if prev_level >= 0:
                    category.parent = categories_map[prev_level][item_number % prev_level_items_count]

                category.save()
                categories_map[level].append(category)

            prev_level_items_count = items_count


class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Organization

    name = factory.Faker('company')
    phones = factory.Faker('phones')
    building = factory.Iterator(Building.objects.order_by('pk').all())

    @classmethod
    def create_batch(cls, size, **kwargs):
        return [cls.create(categories=factory.Faker('category_instances'), **kwargs) for _ in range(size)]

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for category in extracted:
                self.categories.add(category)
