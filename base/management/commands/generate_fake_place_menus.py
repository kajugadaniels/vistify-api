import random
from faker import Faker
from base.models import *
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Generate fake food and drink menus for each place'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Define realistic food and drink menu items
        food_items = [
            "Grilled Chicken", "Cheeseburger", "Spaghetti Bolognese", "Sushi Platter", "Steak with Fries",
            "Vegetable Stir Fry", "Shrimp Tacos", "Margherita Pizza", "Pasta Carbonara", "Caesar Salad",
            "Seafood Paella", "BBQ Ribs", "Chicken Alfredo", "Lobster Bisque", "Beef Kebab", "Pancakes",
            "Club Sandwich", "Vegan Buddha Bowl", "Fish and Chips", "Buffalo Wings", "Stuffed Peppers",
            "Tuna Tartare", "Gnocchi with Pesto", "Duck Confit", "Tiramisu", "Chocolate Lava Cake"
        ]

        drink_items = [
            "Cappuccino", "Espresso", "Latte", "Mocha", "Iced Tea", "Lemonade", "Smoothie", "Fresh Juice",
            "Coca-Cola", "Pepsi", "Sprite", "Tonic Water", "Milkshake", "Cocktail", "Whiskey Sour", "Margarita",
            "Pina Colada", "Martini", "Wine Glass", "Craft Beer", "Mojito", "Rum Punch", "Negroni", "Sangria",
            "Champagne", "Irish Coffee", "Hot Chocolate", "Matcha Latte"
        ]

        places = Place.objects.filter(id__range=(1, 100))  # Fetch all places with IDs from 1 to 100
        total_created = 0

        for place in places:
            menu_items = []

            for _ in range(30):  # Create 30 food items
                menu_items.append(PlaceMenu(
                    place=place,
                    name=random.choice(food_items),
                    description=fake.sentence(nb_words=12),
                    price=round(random.uniform(5, 35), 2)  # Food price range from $5 to $35
                ))

            for _ in range(30):  # Create 30 drink items
                menu_items.append(PlaceMenu(
                    place=place,
                    name=random.choice(drink_items),
                    description=fake.sentence(nb_words=10),
                    price=round(random.uniform(2, 20), 2)  # Drink price range from $2 to $20
                ))

            PlaceMenu.objects.bulk_create(menu_items)  # Bulk create to optimize database inserts
            total_created += len(menu_items)
            self.stdout.write(self.style.SUCCESS(f"Added {len(menu_items)} menu items for {place.name}"))

        self.stdout.write(self.style.SUCCESS(f"Total {total_created} menu items added for {places.count()} places"))
