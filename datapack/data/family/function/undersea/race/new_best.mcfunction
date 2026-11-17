scoreboard players operation @s family.race = #pts family.race_tmp
execute store result storage family:race t.s int 1 run scoreboard players get #s family.race_tmp
execute store result storage family:race t.d int 1 run scoreboard players get #d family.race_tmp
function family:undersea/race/board with storage family:race t
title @s subtitle [{"score": {"name": "#s", "objective": "family.race_tmp"}}, {"text": "."}, {"score": {"name": "#d", "objective": "family.race_tmp"}}, {"text": " seconds: your best!", "color": "white"}]
title @s title {"text":"FINISH!","color":"gold","bold":true}
tellraw @s [{"text": "Driver Finnley", "color": "aqua"}, {"text": ": ", "color": "white"}, {"text": "Whoosh! ", "color": "white"}, {"score": {"name": "#s", "objective": "family.race_tmp"}}, {"text": "."}, {"score": {"name": "#d", "objective": "family.race_tmp"}}, {"text": " seconds, ", "color": "white"}, {"selector": "@s", "color": "white"}, {"text": "! That's your best time yet. It's on the board!", "color": "white"}]
