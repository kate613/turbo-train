from random import randint
import requests

class Pokemon:
    pokemons = {}
    
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer   
        self.pokemon_number = randint(1, 1000)
        self.img = self.get_img()
        self.name = self.get_name()
        self.level = 1  # Начальный уровень
        self.hunger = 0  # Уровень голода (0-100)
        self.experience = 0  # Опыт 
        self.achievements = [] 
        # покемон редким (шанс 5%)
        self.is_rare = self.check_rarity()
        
        Pokemon.pokemons[pokemon_trainer] = self

    def get_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['sprites']['front_default']
        else:
            return "Pikachu"
        
    def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['forms'][0]['name']
        else:
            return "Pikachu"

    def check_rarity(self):
        """Проверяет, является ли покемон редким (5% шанс)"""
        return randint(1, 100) <= 5

    def feed(self):
        """Покормить покемона"""
        if self.hunger >= 20:
            self.hunger -= 20
            self.experience += 10
            
            #  достижения
            self.check_achievements()
            
            #  уровень
            self.check_level_up()
            
            return f"Покемон накормлен! Голод: {self.hunger}%, Опыт: {self.experience}"
        else:
            return "Покемон не голоден!"

    def check_level_up(self):
        """Проверяет, может ли покемон повысить уровень"""
        if self.experience >= self.level * 100:  # Для каждого уровня нужно больше опыта
            self.level += 1
            self.experience = 0
            return f"🎉 Поздравляем! Ваш покемон достиг {self.level} уровня!"
        return None

    def check_achievements(self):
        """Проверяет и добавляет достижения"""
        achievements_to_add = []
        
        if self.level >= 5 and "Новичок" not in self.achievements:
            achievements_to_add.append("Новичок")
        if self.level >= 10 and "Опытный" not in self.achievements:
            achievements_to_add.append("Опытный")
        if self.is_rare and "Счастливчик" not in self.achievements:
            achievements_to_add.append("Счастливчик")
        if len([f for f in range(10)]) >= 10 and "Заботливый" not in self.achievements:
            achievements_to_add.append("Заботливый")
            
        self.achievements.extend(achievements_to_add)
        return achievements_to_add

    def increase_hunger(self):
        """Увеличивает голод покемона (вызывается раз в некоторое время)"""
        self.hunger = min(100, self.hunger + 10)

    def info(self):
        rarity_info = "🌟 РЕДКИЙ ПОКЕМОН! 🌟\n" if self.is_rare else ""
        return f"""{rarity_info}Имя твоего покемона: {self.name}
Уровень: {self.level}
Голод: {self.hunger}%
Опыт: {self.experience}/{self.level * 100}
Достижения: {', '.join(self.achievements) if self.achievements else 'Пока нет'}"""

    def show_img(self):
        return self.img

    def get_super_bonus(self):
        """Супер бонус за редкого покемона"""
        if self.is_rare:
            self.level += 3
            self.achievements.append("Супер сила!")
            return "🎁 ВЫ ПОЛУЧИЛИ СУПЕР БОНУС! +3 уровня к покемону!"
        else:
            return "Этот бонус только для редких покемонов!"
