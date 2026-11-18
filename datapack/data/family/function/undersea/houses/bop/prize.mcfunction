scoreboard players operation @s family.bop_day = #day family.house
give @s minecraft:gold_nugget[item_name={"text": "Sand Dollar", "color": "yellow"},lore=[{"text": "Spend it at the Bubble Cafe", "color": "gray", "italic": false}],custom_data={"family_coin": 1}] 2
tellraw @s [{"text": "Coach Cockle", "color": "red"}, {"text": ": Great bopping, ", "color": "white"}, {"selector": "@s", "color": "white"}, {"text": "! 10 or more! Here are 2 Sand Dollars.", "color": "white"}]
