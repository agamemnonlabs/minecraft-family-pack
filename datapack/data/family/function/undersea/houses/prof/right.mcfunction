scoreboard players operation @s family.riddle_day = #day family.house
give @s minecraft:gold_nugget[item_name={"text": "Sand Dollar", "color": "yellow"},lore=[{"text": "Spend it at the Bubble Cafe", "color": "gray", "italic": false}],custom_data={"family_coin": 1}] 2
execute at @s run playsound minecraft:entity.player.levelup master @s ~ ~ ~
dialog show @s {"type":"minecraft:notice","title":{"text":"Professor Periwinkle","color":"dark_aqua"},"body":[{"type":"minecraft:plain_message","contents":{"text":"That's right! Brilliant! Here are 2 Sand Dollars. Come back tomorrow for a new riddle."}}],"action":{"label":"Yay!"}}
