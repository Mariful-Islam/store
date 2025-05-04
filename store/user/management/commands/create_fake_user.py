from django.core.management import BaseCommand
from tqdm import tqdm
from store.user.models import User
from faker import Faker
from django.db import IntegrityError


faker = Faker()



class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--num-user',
            type=int,
            default=100,
            help='Number of user'
        )
    
    def handle(self, *args, **options):
        num_user = options['num_user']
        
        try:
            for _ in tqdm(range(num_user), desc="Creating user..."):
                user = User.objects.create_user(
                    first_name=faker.first_name(),
                    last_name=faker.last_name(),
                    username=f"{faker.user_name()}_{faker.random_number()}_{_}",
                    role=faker.random_element(elements=('CUSTOMER', 'RETAILER')),
                    phone=faker.phone_number(),
                    address=faker.address(),
                    email=faker.email()
                    
                )

                user.set_password("1234")

                user.save()

                self.stdout.write(self.style.SUCCESS(f'{user.username} is created...'))

        except IntegrityError as e:
            self.stdout.write(self.style.ERROR(f'Error creating post: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Unexpected error: {e}'))