execute in family:undersea as @a[distance=0..] at @s run function family:undersea/raid/fx/win
execute in family:undersea run particle minecraft:totem_of_undying -167.5 42 -143.5 4 3 4 0.6 100 force
execute in family:undersea run tellraw @a[distance=0..] [{"text": "Mayor Marina", "color": "light_purple"}, {"text": ": Hooray! You saved the town! Here are 3 Sand Dollars for every defender!", "color": "white"}]
execute as @a[tag=family.raid.in] run give @s minecraft:gold_nugget[item_name={"text": "Sand Dollar", "color": "yellow"},lore=[{"text": "Spend it at the Bubble Cafe", "color": "gray", "italic": false}],custom_data={"family_coin": 1}] 3
function family:undersea/raid/finish
