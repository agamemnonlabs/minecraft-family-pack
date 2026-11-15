execute unless entity @e[type=minecraft:marker,tag=family.portal_down,distance=..8] run return run tellraw @s {"text": "Stand next to a whirlpool first.", "color": "yellow"}
execute at @n[type=minecraft:marker,tag=family.portal_down,distance=..8] positioned ~ ~1.5 ~ align xyz run function family:undersea/plaza
tellraw @s {"text": "Plaza and beacon built around the whirlpool.", "color": "aqua"}
