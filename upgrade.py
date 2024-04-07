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
            "max_velocity": 0,
            "rotation_speed": 0,
            "can_slow_down": 0,
            "grabber_speed": 0,
            "grabber_length": 0,
            "shield": 0,
            "ee": 0
        }
        self.max_upgrades: dict[str, int] = {
            "max_velocity": 4,
            "rotation_speed": 2,
            "can_slow_down": 1,
            "grabber_speed": 2,
            "grabber_length": 4,
            "shield": 2,
            "ee": 1
        }
        self.upgrade_cost: dict[str, list[int]] = {
            "max_velocity": [100, 130, 185, 234],
            "rotation_speed": [310, 420],
            "can_slow_down": [240],
            "grabber_speed": [100, 150],
            "grabber_length": [145, 187, 252, 301],
            "shield": [160, 330],
            "ee": [700]
        }
        self.upgrade_values: dict[str, list[float | bool]] = {
            "max_velocity": [3.3, 3.8, 4.3, 4.9, 5.4],
            "rotation_speed": [2, 2.7, 3.5],
            "can_slow_down": [False, True],
            "grabber_speed": [5, 9, 13],
            "grabber_length": [0, 1, 2, 3, 4],
            "shield": [0, 1, 2],
            "ee": [False, True]
        }
        self.upgrade_display: dict[str, tuple[str, str]] = {
            "max_velocity": ("Sebesség", "Megnöveli az űrhajó \nmaximális sebességét"),
            "rotation_speed": ("Forgási sebesség", "Megnöveli az űrhajó \nforgásának sebességét"),
            "can_slow_down": ("Lassítás", "Az űrhajó le tud lassítani \n(S vagy Lefele Nyíl)"),
            "grabber_speed": ("Kar sebessége", "Megnöveli az űrhajó \nkarjának kinyúlási és \nvisszahúzódási sebességét"),
            "grabber_length": ("Kar hossza", "Megnöveli az űrhajó \nkarjának hosszát"),
            "shield": ("Pajzs", "Megvédi az űrhajót a \nmeteoroktól egy alkalommal"),
            "ee": ("???", "?????")
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

        print("Bought upgrade", upgrade_name, "for", cost, "points")

        return cost

    def get_random_upgrades(self, amount: int) -> list[tuple[str, int, int]]:
        upgrades: set[tuple[str, int, int]] = set()

        ee: bool = random.randint(0, 4) == 0

        limit: int = 100
        while len(upgrades) < amount and limit > 0:
            limit -= 1
            upgrade: str = random.choice(list(self.upgrades.keys()))

            if upgrade == "ee" and not ee:
                continue

            if self.is_maxed(upgrade):
                continue

            upgrades.add((upgrade, self.upgrades[upgrade],
                          self.upgrade_cost[upgrade][self.upgrades[upgrade]]))
        return list(upgrades)
