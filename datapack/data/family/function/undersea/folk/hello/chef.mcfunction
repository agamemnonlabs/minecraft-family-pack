tag @s add family.met.chef
execute if score #night family.alive matches 1 run return run tellraw @s [{"text": "Chef Clamuel", "color": "gold"}, {"text": ": Zzz... mmm, coral cookies... (Chef Clamuel is fast asleep. The cafe opens again at sunrise!)", "color": "white"}]
tellraw @s [{"text": "Chef Clamuel", "color": "gold"}, {"text": ": Welcome to the Bubble Cafe, ", "color": "white"}, {"selector": "@s", "color": "white"}, {"text": "! Tap me for snacks, or tap my bell for a delivery job.", "color": "white"}]
playsound minecraft:entity.villager.ambient neutral @s ~ ~ ~
