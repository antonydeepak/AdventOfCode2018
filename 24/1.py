import re

class Group(object):
    def __init__(self, units, hit_point, attack_damage, attack_type, initiative, weaknesses, immunities):
        self.hit_point = hit_point
        self.attack_damage = attack_damage
        self.attack_type = attack_type
        self.initiative = initiative
        self.weaknesses = weaknesses
        self.immunities = immunities
        self.units = units
    
    @property
    def effective_power(self):
        return self.units * self.attack_damage

    def hit(self, damage):
        units_damaged = damage // self.hit_point
        self.units = max(0, self.units-units_damaged)

def get_target_selection_order(groups):
    # groups has units
    def score(group):
        return (group.effective_power, group.initiative)
    
    return sorted(groups, key=lambda x: score(x), reverse=True)

def select_target(attacking_group, defending_army):
    def score(defending_group):
        damage = attacking_group.effective_power * (2 if attacking_group.attack_type in defending_group.weaknesses else 1)
        return (damage, defending_group.effective_power, defending_group.initiative)
    
    potential_targets = (group for group in defending_army if attacking_group.attack_type not in group.immunities)
    targets = sorted(potential_targets, key=lambda x: score(x), reverse=True)
    return targets[0] if len(targets)>0 else None

def get_attack_order(groups):
    def score(group):
        return (group.initiative)
    
    return sorted(groups, key=lambda x: score(x), reverse=True)

def attack(attacking_group, defending_group):
    if not (attacking_group and defending_group):
        return
    damage = attacking_group.effective_power * (2 if attacking_group.attack_type in defending_group.weaknesses else 1)
    defending_group.hit(damage)

def parse(line):
    required = re.search(r"(\d+) units each with (\d+) hit points.*with an attack that does (\d+) (\w+) damage at initiative (\d+)", line)
    immune  = re.search(r"immune to (.*?)[;\)]", line)
    immunity = []
    if immune:
        text = immune.groups()[0]
        immunity = re.findall(r"(\w+)", text)
    weak  = re.search(r"weak to (.*?)\)", line)
    weakness = []
    if weak:
        text = weak.groups()[0]
        weakness = re.findall(r"(\w+)", text)
    return int(required[1]),int(required[2]),int(required[3]),required[4],int(required[5]),weakness,immunity

if __name__ == "__main__":
    # file_name = "./24/test.in"
    file_name = "./24/1.in"
    lines = open(file_name, 'r').readlines()

    immune_army = set()
    infect_army = set()
    current_army = None
    for line in lines:
        line = line.rstrip()
        if "Immune System" in line:
            current_army = immune_army
            continue
        if "Infection" in line:
            current_army = infect_army
            continue
        values = parse(line)
        current_army.add(Group(*values))

    while len(immune_army)>0 and len(infect_army)>0:
        groups = immune_army.union(infect_army)
        targets = {}
        # select
        for attacking_group in get_target_selection_order(groups):
            defending_army = immune_army if attacking_group in infect_army else infect_army
            unchosen_targets = (group for group in defending_army if group not in targets.values())
            defending_group = select_target(attacking_group, unchosen_targets)
            targets[attacking_group] = defending_group
        
        # attack
        for attacking_group in get_attack_order(groups):
            defending_group = targets[attacking_group]
            attack(attacking_group, defending_group)
        
        # prune
        immune_army = set((group for group in immune_army if group.units>0))
        infect_army = set((group for group in infect_army if group.units>0))
    
    # of the army should have 0 units
    print(sum(group.units for group in immune_army) + sum(group.units for group in infect_army))