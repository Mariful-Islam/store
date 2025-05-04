from django.core.management import BaseCommand
from faker import Faker
from store.order.models import Order, OrderItem
from store.product.models import Product, ProductVariant
from tqdm import tqdm
from django.db import IntegrityError
from decimal import Decimal
from store.user.models import User




faker = Faker()

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--num-order',
            type=int,
            default=50,
            help="Num of posts"
        )
    
    def handle(self, *args, **options):
        num_order = options['num_order']
        try:
            for i in tqdm(range(num_order), desc="Create order"):
                # customer = User.objects.create_user(
                #     first_name=faker.first_name(),
                #     last_name=faker.last_name(),
                #     username=f"{faker.user_name()}_{faker.random_number()}_{_}",
                #     role='CUSTOMER',
                #     phone=faker.phone_number(),
                #     address=faker.address(),
                #     email=faker.email()
                    
                # )

                # retailer = User.objects.create_user(
                #     first_name=faker.first_name(),
                #     last_name=faker.last_name(),
                #     username=f"{faker.user_name()}_{faker.random_number()}_{_}",
                #     role='RETAILER',
                #     phone=faker.phone_number(),
                #     address=faker.address(),
                #     email=faker.email()
                    
                # )

                # customer.set_password("1234")
                # retailer.set_password("1234")
                # customer.save()
                # retailer.save()

                order = Order.objects.create(
                    customer = faker.random_element(elements=User.objects.filter(role='CUSTOMER')),
                    retailer = faker.random_element(elements=User.objects.filter(role='CUSTOMER')),
                    total_price = faker.random_number(),
                    total_qty = faker.random_number()
                )
                
                order.save()


                for j in tqdm(range(4), desc=f"Creating {order.id}'s variants...."):
                    
                    order_item = OrderItem.objects.create(
                        order = order,
                        product_variant = faker.random_element(elements=ProductVariant.objects.all()),
                        quantity = faker.random_int(min=1, max=50),
                        price = Decimal(faker.pyfloat(left_digits=4, right_digits=2, positive=True, min_value=1.00, max_value=9999.99)),
                        
                    )

                    order_item.save()

                    self.stdout.write(self.style.SUCCESS(f"{order_item.id} is created."))
            
        except IntegrityError as e:
            self.stdout.write(self.style.ERROR(f'Error creating post: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Unexpected error: {e}'))
