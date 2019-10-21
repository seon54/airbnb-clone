import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms.models import Room, RoomType, Photo, Amenity, Facility, HouseRule
from users.models import User

NAME = 'rooms'


class Command(BaseCommand):
    help = f'This command creates many {NAME}'

    def add_arguments(self, parser):
        parser.add_argument('--number', default=2, type=int, help=f'How many {NAME} do you want to create?')

    def handle(self, *args, **options):
        number = options.get('number')
        seeder = Seed.seeder()
        all_users = User.objects.all()
        room_types = RoomType.objects.all()
        seeder.add_entity(Room, number, {
            'name': lambda x: seeder.faker.address(),
            'host': lambda x: random.choice(all_users),
            'room_type': lambda x: random.choice(room_types),
            'price': lambda x: random.randint(5000, 50000),
            'guest': lambda x: random.randint(1, 10),
            'beds': lambda x: random.randint(1, 5),
            'bedrooms': lambda x: random.randint(1, 5),
            'baths': lambda x: random.randint(1, 5)
        })
        created_photos = seeder.execute()
        created_clean = flatten(list(created_photos.values()))
        amenities = Amenity.objects.all()
        facilities = Facility.objects.all()
        rules = HouseRule.objects.all()
        for pk in created_clean:
            room = Room.objects.get(pk=pk)
            for i in range(3, random.randint(10, 30)):
                Photo.objects.create(caption=seeder.faker.sentence(),
                                     room=room,
                                     file=f'room_photos/{random.randint(1, 31)}.webp')
            for a in amenities:
                num = random.randint(0, 15)
                if num % 2 == 0:
                    room.amenities.add(a)
            for f in facilities:
                num = random.randint(0, 15)
                if num % 2 == 0:
                    room.facilities.add(f)
            for r in rules:
                num = random.randint(0, 15)
                if num % 2 == 0:
                    room.rules.add(r)
        self.stdout.write(self.style.SUCCESS(f'{number} {NAME} created.'))
