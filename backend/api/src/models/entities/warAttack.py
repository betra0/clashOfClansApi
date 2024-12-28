class WarAttack:
    def __init__(self, 
                 attackerTag, 
                 defenderTag, 
                 stars, 
                 destructionPercentage, 
                 order, 
                 duration):
        self.id = f"{attackerTag}_{defenderTag}_{order}_{duration}"
        self.attackerTag = attackerTag
        self.defenderTag = defenderTag
        self.stars = stars
        self.destructionPercentage = destructionPercentage
        self.order = order
        self.duration = duration

    def __eq__(self, other):
        return isinstance(other, WarAttack) and self.id == other.id

    def __hash__(self):
        return hash(self.id)
    
    def getdict(self, notNull=False):
        data = {
        'id': self.id,
        'stars': self.stars,
        'destructionPercentage': self.destructionPercentage,
        'order': self.order,
        'duration': self.duration
        }

        # Si `notNull` es True, excluye las claves con valores `None`
        if notNull:
            data = {key: value for key, value in data.items() if value is not None}

        return data