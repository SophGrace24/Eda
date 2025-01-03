class VirtualGarden:
    def __init__(self):
        self.plants = []
        self.progress = 0

    def add_plant(self, plant_type):
        self.plants.append({
            'type': plant_type,
            'growth': 0
        })
        self.progress += 1

    def view_garden(self):
        return {
            'plants': self.plants,
            'progress': self.progress
        }

    def grow_plants(self):
        for plant in self.plants:
            if plant['growth'] < 100:
                plant['growth'] += 10
