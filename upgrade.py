class UpgradeManager:
    @property
    def get_upgrades_to_show(self) -> list[tuple[str, int, int | None]]:
        upgrade_list: list[tuple[str, int, int | None]] = []
        for upgrade, value in self.upgrades.items():
            upgrade_list.append((upgrade, value,
                                 self.upgrade_cost[upgrade][value] if value != self.max_upgrades[upgrade] else None))
        return upgrade_list

    def __init__(self, upgrades: dict[str, int]) -> None:
        self.upgrades: dict[str, int] = {
            "max_velocity": 0,
            "acceleration": 0,
            "rotation_speed": 0,
            "can_slow_down": 0,
            "grabber_speed": 0,
            "grabber_length": 0
        }
        self.max_upgrades: dict[str, int] = {
            "max_velocity": 4,
            "acceleration": 2,
            "rotation_speed": 2,
            "can_slow_down": 1,
            "grabber_speed": 2,
            "grabber_length": 4
        }
        self.upgrade_cost: dict[str, list[int]] = {
            "max_velocity": [100, 130, 185, 234],
            "acceleration": [240, 315],
            "rotation_speed": [310, 420],
            "can_slow_down": [560],
            "grabber_speed": [60, 100],
            "grabber_length": [145, 187, 252, 301]
        }

        self.upgrades.update(upgrades)
        for upgrade, value in self.upgrades.items():
            self.upgrades[upgrade] = min(value, self.max_upgrades[upgrade])

    def try_buy(self, upgrade_name: str, points: int) -> bool:
        upgrade_level: int = self.upgrades[upgrade_name]
        if self.upgrade_cost[upgrade_name][upgrade_level] < points:
            return False
        elif upgrade_level == self.max_upgrades[upgrade_name]:
            return False

        self.upgrades[upgrade_name] += 1
        return True
