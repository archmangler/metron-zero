import pygame
from config import *

class Weapon:
    def __init__(self, name, damage, price, range=50):
        self.name = name
        self.damage = damage
        self.price = price
        self.range = range
        self.cooldown = 30  # Frames between attacks
        self.current_cooldown = 0

    def can_attack(self):
        return self.current_cooldown <= 0

    def update(self):
        if self.current_cooldown > 0:
            self.current_cooldown -= 1

class WeaponManager:
    @staticmethod
    def create_weapon(weapon_data):
        return Weapon(
            name=weapon_data['name'],
            damage=weapon_data['damage'],
            price=weapon_data['price']
        )

    @staticmethod
    def get_default_weapons():
        return [
            {
                'name': 'Short Sword',
                'damage': 15,
                'price': 100,
                'range': 50
            },
            {
                'name': 'Battle Axe',
                'damage': 25,
                'price': 200,
                'range': 45
            },
            {
                'name': 'Magic Staff',
                'damage': 20,
                'price': 150,
                'range': 100
            }
        ]
