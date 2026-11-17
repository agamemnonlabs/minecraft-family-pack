advancement revoke @s only family:folk/tap_pearl10
execute if entity @s[tag=family.found.pearl10] run return run title @s actionbar [{"text": "You already found this pearl: ", "color": "gold"}, {"score": {"name": "@s", "objective": "family.pearls"}, "color": "gold"}, {"text": " of 10", "color": "gold"}]
tag @s add family.found.pearl10
scoreboard players add @s family.pearls 1
execute in family:undersea positioned -138.5 57.5 -162.5 run particle minecraft:end_rod ~ ~ ~ 0.4 0.4 0.4 0.05 25
execute in family:undersea positioned -138.5 57.5 -162.5 run playsound minecraft:block.amethyst_block.chime master @s ~ ~ ~ 1 1.2
title @s actionbar [{"text": "Golden pearl! ", "color": "gold"}, {"score": {"name": "@s", "objective": "family.pearls"}, "color": "gold"}, {"text": " of 10", "color": "gold"}]
execute if score @s family.pearls matches 10 run tellraw @s [{"text": "Mayor Marina", "color": "light_purple"}, {"text": ": You found all 10?! Come and see me by the welcome arch!", "color": "white"}]
