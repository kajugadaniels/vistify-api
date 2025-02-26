import random
from faker import Faker
from base.models import *
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Generate 100 fake entertainment tags'

    def handle(self, *args, **kwargs):
        fake = Faker()
        # Base entertainment topics
        base_tags = [
            "Dancing", "Drinking", "Date Nights", "Kizomba Dance", "Working Out", "Singing", "Concert",
            "Karaoke", "Nightlife", "Partying", "Movie Buff", "Theater", "Comedy", "Standup", "DJ",
            "Clubbing", "Art", "Gallery", "Exhibition", "Museum", "Fashion", "Runway", "Modeling", "Festival",
            "Carnival", "Music", "Beats", "Jam Session", "Chill", "Vibes", "Foodie", "Gourmet", "Culinary",
            "Barbecue", "Happy Hour", "Mixology", "Lounge", "Wine Tasting", "Craft Beer", "Sports", "Fitness",
            "Gym", "Yoga", "Pilates", "Zumba", "Jazz", "Blues", "Hip Hop", "R&B", "Pop", "Rock", "Electronic",
            "Indie", "Acoustic", "Classical", "Opera", "Disco", "Salsa", "Tango", "Swing", "House Party",
            "Open Mic", "Poetry", "Storytelling", "Live Performance", "DJ Night", "House Music", "Reggae",
            "Dubstep", "EDM", "Festival Vibes", "After Party", "Chillout", "Road Trip", "Adventure",
            "Escape Room", "Virtual Reality", "Arcade", "Sports Bar", "Dinner", "Date", "Love", "Romance",
            "Speed Dating", "Socializing", "Mixer", "Club", "Rooftop", "Sunset", "Sunrise", "Beach Party",
            "Pool Party", "Fun", "Excitement", "Hype", "Vibe", "Celebration", "Bonfire", "Game Night",
            "Trivia", "Board Games", "Dance Battle", "Lip Sync", "Jam", "Live Band", "Concert Night",
            "Ultimate Party", "Midnight Snack", "Electric", "Groove", "Funk", "Underground", "Street Food",
            "Mingle", "Fusion", "Eclectic", "Urban", "Boogie"
        ]
        
        created_count = 0
        used_names = set()
        while created_count < 100:
            base_tag = random.choice(base_tags)
            if random.choice([True, False]):
                adjective = fake.word().capitalize()
                tag_name = f"{adjective} {base_tag}"
            else:
                number = random.randint(1, 999)
                tag_name = f"{base_tag} {number}"
            # Ensure the tag name is unique.
            if tag_name in used_names:
                continue
            used_names.add(tag_name)
            Tag.objects.create(name=tag_name)
            created_count += 1
            self.stdout.write(self.style.SUCCESS(f"Created tag: {tag_name}"))
        
        self.stdout.write(self.style.SUCCESS(f"Total new tags created: {created_count}"))
