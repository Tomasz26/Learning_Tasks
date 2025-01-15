import json
import random


class Watchlist:
    def __init__(self):
        try:
            with open("towatchs.json", "r") as f:
                self.towatch = json.load(f)
        except FileNotFoundError:
            self.towatch = []

    def all(self):
        return self.towatch

    def get(self, id):
        return self.towatch[id]

    def create(self, data):
        if 'csrf_token' in data:
            data.pop('csrf_token')
        if self.towatch:
            max_id = max(item.get('id', 0) for item in self.towatch)
        else:
            max_id = 0
        data['id'] = max_id + 1
        self.towatch.append(data)
        self.save_all()

    def save_all(self):
        with open("towatchs.json", "w") as f:
            json.dump(self.towatch, f)

    def update(self, id, data):
        if 'csrf_token' in data:
            data.pop('csrf_token')
        towatchid = self.get(id)
        if towatchid:
            index = self.towatch.index(towatchid)
            self.towatch[index] = data
            self.save_all()
            return True
        return False

    def get(self, id):
        towatchid = [towatchid for towatchid in self.all() if towatchid['id'] == id]
        if towatchid:
            return towatchid[0]
        return []
    
    def delete(self, id):
        towatchid = self.get(id)
        if towatchid:
            self.towatch.remove(towatchid)
            self.save_all()
            return True
        return False
    
    def choose_random_movie(self):
        random_movie = random.choice(self.towatch) 
        while random_movie['done'] == True:
            random_movie = random.choice(self.towatch)
        return random_movie

towatch = Watchlist()