from faker import Faker
from base.models import *
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Generate 40 fake entertainment categories'

    def handle(self, *args, **kwargs):
        fake = Faker()
        entertainment_categories = [
            "Hotel", "Bar", "Restaurant", "Gym", "Night Club", "Cinema",
            "Spa", "Arcade", "Theater", "Lounge", "Café", "Pub", "Resort",
            "Disco", "Karaoke", "Bowling Alley", "Brewery", "Live Music Venue",
            "Casino", "Rooftop Bar", "Jazz Club", "Comedy Club", "Dance Studio",
            "Pool Lounge", "Dinner Theater", "Sports Bar", "Steakhouse", "Pizzeria",
            "Ice Rink", "Concert Hall", "Night Bazaar", "Wine Bar", "Bistro",
            "Burger Joint", "Sushi Bar", "Taco Stand", "Art Gallery", "Museum",
            "Escape Room", "Virtual Reality Arcade", "Church"
        ]

        created_count = 0
        for name in entertainment_categories:
            if not Category.objects.filter(name=name).exists():
                Category.objects.create(
                    name=name,
                    description=fake.paragraph(nb_sentences=3)
                )
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Created category: {name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Category already exists: {name}"))
        self.stdout.write(self.style.SUCCESS(f"Total new categories created: {created_count}"))
