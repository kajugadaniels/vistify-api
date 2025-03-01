from base.models import *
import random
from faker import Faker
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Generate 100 fake places with realistic Rwanda locations and images."

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Rwanda location data (real provinces, districts, sectors, cells, villages)
        locations = [
            {"province": "Kigali", "district": "Gasabo", "sector": "Remera", "cell": "Nyabisindu", "village": "Ubumwe"},
            {"province": "Kigali", "district": "Kicukiro", "sector": "Nyarugunga", "cell": "Kabeza", "village": "Kamashashi"},
            {"province": "Kigali", "district": "Nyarugenge", "sector": "Kimisagara", "cell": "Kora", "village": "Gitega"},
            {"province": "Northern", "district": "Musanze", "sector": "Muhoza", "cell": "Cyabararika", "village": "Kigombe"},
            {"province": "Western", "district": "Rubavu", "sector": "Gisenyi", "cell": "Mbugangari", "village": "Nyirakigugu"},
            {"province": "Eastern", "district": "Rwamagana", "sector": "Muhazi", "cell": "Gahengeri", "village": "Kiruhura"},
            {"province": "Southern", "district": "Huye", "sector": "Ngoma", "cell": "Tumba", "village": "Umucyo"},
        ]

        # Fetch existing categories and tags
        categories = list(Category.objects.all())
        tags = list(Tag.objects.all())

        if not categories or not tags:
            self.stdout.write(self.style.ERROR("Please generate categories and tags before creating places."))
            return

        places_created = 0

        for _ in range(100):
            # Select random location
            location = random.choice(locations)

            # Generate a random place name
            place_name = fake.company() + " " + random.choice(["Bar", "Lounge", "Restaurant", "Hotel", "Resort", "Club", "Gym", "Cinema"])

            # Select a random category
            category = random.choice(categories)

            # Select random tags (1 to 4)
            selected_tags = random.sample(tags, random.randint(1, 4))

            # Create the place
            place = Place.objects.create(
                name=place_name,
                description=fake.paragraph(nb_sentences=5),
                category=category,
                province=location["province"],
                district=location["district"],
                sector=location["sector"],
                cell=location["cell"],
                village=location["village"],
                address=fake.street_address(),
                latitude=random.uniform(-2.00, -1.00),
                longitude=random.uniform(29.00, 30.00),
                views=random.randint(100, 5000),
            )
            
            # Attach tags
            place.tags.set(selected_tags)

            # Generate random fake images for the place
            for _ in range(random.randint(1, 3)):  # 1 to 3 images per place
                fake_image_url = f"https://via.placeholder.com/1080x600/{random.choice(['ff5733', '33ff57', '3357ff', 'ff33a8', 'a833ff'])}/ffffff?text={place.name.replace(' ', '+')}"
                PlaceImage.objects.create(place=place, image=fake_image_url, caption=fake.sentence())

            places_created += 1
            self.stdout.write(self.style.SUCCESS(f"Created place: {place.name}"))

        self.stdout.write(self.style.SUCCESS(f"Total new places created: {places_created}"))
