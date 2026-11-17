scoreboard players enable @s family.talk
execute if entity @s[tag=family.racing] run return run dialog show @s {"type":"minecraft:multi_action","title":{"text":"Driver Finnley","color":"aqua"},"body":[{"type":"minecraft:plain_message","contents":{"text":"You're in the middle of a race! Do you want to stop?"}}],"columns":1,"actions":[{"label":"Stop racing","action":{"type":"minecraft:run_command","command":"/trigger family.talk set 7"}}],"exit_action":{"label":"Keep racing"}}
execute unless score @s family.race matches 0.. run return run dialog show @s {"type":"minecraft:multi_action","title":{"text":"Driver Finnley","color":"aqua"},"body":[{"type":"minecraft:plain_message","contents":{"text":"Beep beep! Want to race the Current Race? Swim through the START gate, then through all 11 hoops in order (number 10 is the welcome arch), and back through the gate. Follow the sparkles!"}}],"columns":1,"actions":[{"label":"Let's race!","action":{"type":"minecraft:run_command","command":"/trigger family.talk set 5"}},{"label":"How does it work?","action":{"type":"minecraft:run_command","command":"/trigger family.talk set 6"}}],"exit_action":{"label":"Not now"}}
scoreboard players operation #b family.race_tmp = #base family.race_tmp
scoreboard players operation #b family.race_tmp -= @s family.race
scoreboard players operation #bs family.race_tmp = #b family.race_tmp
scoreboard players operation #bs family.race_tmp /= #10 family.race_tmp
scoreboard players operation #bd family.race_tmp = #b family.race_tmp
scoreboard players operation #bd family.race_tmp %= #10 family.race_tmp
execute store result storage family:race me.s int 1 run scoreboard players get #bs family.race_tmp
execute store result storage family:race me.d int 1 run scoreboard players get #bd family.race_tmp
function family:undersea/race/menu_best with storage family:race me
