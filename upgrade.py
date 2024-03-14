import random


class UpgradeManager:
    @property
    def get_upgrades_to_show(self) -> list[tuple[str, int, int | None]]:
        upgrade_list: list[tuple[str, int, int | None]] = []
        for upgrade, value in self.upgrades.items():
            upgrade_list.append((upgrade, value,
                                 self.upgrade_cost[upgrade][value] if value != self.max_upgrades[upgrade] else None))
        return upgrade_list

    @property
    def get_upgrade_values(self) -> dict[str, float | bool]:
        upgrade_values: dict[str, float | bool] = {}
        for upgrade, value in self.upgrades.items():
            upgrade_values[upgrade] = self.upgrade_values[upgrade][value]
        return upgrade_values

    def __init__(self, upgrades: dict[str, int]) -> None:
        self.upgrades: dict[str, int] = {
            "max velocity": 0,
            "acceleration": 0,
            "rotation speed": 0,
            "can slow down": 0,
            "grabber speed": 0,
            "grabber length": 0
        }
        self.max_upgrades: dict[str, int] = {
            "max velocity": 4,
            "acceleration": 2,
            "rotation speed": 2,
            "can slow down": 1,
            "grabber speed": 2,
            "grabber length": 4
        }
        self.upgrade_cost: dict[str, list[int]] = {
            "max velocity": [100, 130, 185, 234],
            "acceleration": [240, 315],
            "rotation speed": [310, 420],
            "can slow down": [240],
            "grabber speed": [100, 150],
            "grabber length": [145, 187, 252, 301]
        }
        self.upgrade_values: dict[str, list[float | bool]] = {
            "max velocity": [3, 3.3, 3.5, 3.8, 4.2],
            "acceleration": [0.5, 0.8, 1],
            "rotation speed": [2, 2.7, 3.5],
            "can slow down": [False, True],
            "grabber speed": [5, 9, 13],
            "grabber length": [0, 1, 2, 3, 4]
        }

        self.upgrades.update(upgrades)
        for upgrade, value in self.upgrades.items():
            self.upgrades[upgrade] = min(value, self.max_upgrades[upgrade])

    def is_maxed(self, upgrade_name: str) -> bool:
        return self.upgrades[upgrade_name] == self.max_upgrades[upgrade_name]

    def can_buy(self, upgrade_name: str, points: int) -> bool:
        upgrade_level: int = self.upgrades[upgrade_name]

        if upgrade_level == self.max_upgrades[upgrade_name]:
            return False
        elif self.upgrade_cost[upgrade_name][upgrade_level] > points:
            return False

        return True

    def try_buy(self, upgrade_name: str, points: int) -> int:
        if not self.can_buy(upgrade_name, points):
            return 0

        cost: int = self.upgrade_cost[upgrade_name][self.upgrades[upgrade_name]]
        self.upgrades[upgrade_name] += 1
        return cost

    def get_random_upgrades(self, amount: int) -> list[tuple[str, int, int]]:
        upgrades: set[tuple[str, int, int]] = set()

        limit: int = 100
        while len(upgrades) < amount and limit > 0:
            limit -= 1
            upgrade: str = random.choice(list(self.upgrades.keys()))

            if self.is_maxed(upgrade):
                continue

            upgrades.add((upgrade, self.upgrades[upgrade],
                          self.upgrade_cost[upgrade][self.upgrades[upgrade]]))
        return list(upgrades)
