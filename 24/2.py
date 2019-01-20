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

def solve_part_1(lines, boost):
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

    # boost
    for group in immune_army:
        group.attack_damage += boost

    while len(immune_army)>0 and len(infect_army)>0:
        groups = immune_army.union(infect_army)
        targets = {}
        # select
        for attacking_group in get_target_selection_order(groups):
            defending_army = immune_army if attacking_group in infect_army else infect_army
            unchosen_targets = (group for group in defending_army if group not in targets.values())
            defending_group = select_target(attacking_group, unchosen_targets)
            targets[attacking_group] = defending_group
        
        # no attack possible
        if len([v for v in targets.values() if v]) == 0:
            raise "stalemate"

        # attack
        for attacking_group in get_attack_order(groups):
            defending_group = targets[attacking_group]
            attack(attacking_group, defending_group)
        
        # prune
        immune_army = set((group for group in immune_army if group.units>0))
        infect_army = set((group for group in infect_army if group.units>0))

    return immune_army

if __name__ == "__main__":
    # file_name = "./24/test.in"
    file_name = "./24/1.in"
    lines = open(file_name, 'r').readlines()

    boost_min = 1
    boost_max = 50000 #guestimate

    # binary search the optimal boost
    while boost_min<boost_max:
        boost = (boost_min+boost_max) // 2
        print(boost_min, boost_max, boost)

        try:
            immune_army = solve_part_1(lines, boost)
        except: #stalement
            immune_army = []
    
        if sum(group.units for group in immune_army)>0: # won
            boost_max = boost
        else: # lost
            boost_min = boost+1

    result = sum(group.units for group in solve_part_1(lines, boost_max)) # boost_max is the best
    assert(result>0) #wrong guesstimate
    print(result)