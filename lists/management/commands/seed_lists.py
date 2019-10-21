import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from lists.models import List
from users.models import User
from rooms.models import Room

NAME = 'lists'


class Command(BaseCommand):
    help = f'This command creates {NAME}'

    def add_arguments(self, parser):
        parser.add_argument('--number', default=2, type=int, help=f'How many {NAME} do you want to create?')

    def handle(self, *args, **options):
        number = options.get('number')
        seeder = Seed.seeder()
        users = User.objects.all()
        rooms = Room.objects.all()
        seeder.add_entity(List, number, {
            'user': lambda x: random.choice(users)
        })
        created_lists = seeder.execute()
        cleaned_lists = flatten(list(created_lists.values()))
        for pk in cleaned_lists:
            list_obj = List.objects.get(pk=pk)
            to_add = rooms[random.randint(0, 5): random.randint(6, 30)]
            list_obj.rooms.add(*to_add)
        self.stdout.write(self.style.SUCCESS(f'{number} {NAME} created.'))
