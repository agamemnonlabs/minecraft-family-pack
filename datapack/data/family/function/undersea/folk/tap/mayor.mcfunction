advancement revoke @s only family:folk/tap_mayor
execute if items entity @s container.* minecraft:bowl[minecraft:custom_data~{family_to:"mayor"}] run return run function family:undersea/folk/deliver/mayor
execute if items entity @s weapon.offhand minecraft:bowl[minecraft:custom_data~{family_to:"mayor"}] run return run function family:undersea/folk/deliver/mayor
scoreboard players enable @s family.talk
execute if entity @s[tag=family.pearls_done] run return run dialog show @s {"type":"minecraft:notice","title":{"text":"Mayor Marina","color":"light_purple"},"body":[{"type":"minecraft:plain_message","contents":{"text":"Thank you again for finding my golden pearls! Our town is lucky to have you."}}],"action":{"label":"Bye!"}}
execute if score @s family.pearls matches 10.. run return run dialog show @s {"type":"minecraft:multi_action","title":{"text":"Mayor Marina","color":"light_purple"},"body":[{"type":"minecraft:plain_message","contents":{"text":"You found all 10 of my golden pearls! Thank you so much! I have a reward for you."}}],"columns":1,"actions":[{"label":"Yay! Thank you!","action":{"type":"minecraft:run_command","command":"/trigger family.talk set 3"}}],"exit_action":{"label":"Later"}}
execute store result storage family:folk pearls.n int 1 run scoreboard players get @s family.pearls
function family:undersea/folk/mayor_ask with storage family:folk pearls
