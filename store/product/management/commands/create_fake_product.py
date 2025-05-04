from django.core.management import BaseCommand
from faker import Faker
from store.product.models import Product, ProductVariant
from tqdm import tqdm
from django.db import IntegrityError
from decimal import Decimal


faker = Faker()

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--num-product',
            type=int,
            default=30,
            help="Num of posts"
        )
    
    def handle(self, *args, **options):
        num_product = options['num_product']
        try:
            for i in tqdm(range(num_product), desc="Create product"):
                product = Product.objects.create(
                    name = faker.name(),
                    description = faker.sentence(),
                    slug = faker.slug(),
                    category = faker.name()
                )
                
                product.save()

                for j in tqdm(range(4), desc=f"Creating {product.name}'s variants...."):
                    variant = ProductVariant.objects.create(
                        name = faker.name(),
                        product = product,
                        sku = f"{product.name}-{product.category}-{j}",
                        price = Decimal(faker.pyfloat(left_digits=4, right_digits=2, positive=True, min_value=1.00, max_value=9999.99)),
                        stock = faker.random_int(min=1, max=500),
                        attribute = {
                            "color": faker.color(),
                            "size": faker.random_number(),
                            "type": faker.name()
                        }
                    )

                    variant.save()


                    self.stdout.write(self.style.SUCCESS(f"{product.name} is created."))
            
        except IntegrityError as e:
            self.stdout.write(self.style.ERROR(f'Error creating post: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Unexpected error: {e}'))
