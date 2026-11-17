clear @s minecraft:bowl[minecraft:custom_data~{family_to:"mayor"}] 1
give @s minecraft:gold_nugget[item_name={"text": "Sand Dollar", "color": "yellow"},lore=[{"text": "Spend it at the Bubble Cafe", "color": "gray", "italic": false}],custom_data={"family_coin": 1}] 3
tellraw @s [{"text": "Mayor Marina", "color": "light_purple"}, {"text": ": Lunch from the Bubble Cafe? Yum! Thank you, ", "color": "white"}, {"selector": "@s", "color": "white"}, {"text": "! Here are 3 Sand Dollars.", "color": "white"}]
playsound minecraft:entity.villager.yes neutral @s ~ ~ ~
