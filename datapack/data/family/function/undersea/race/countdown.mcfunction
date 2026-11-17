scoreboard players remove @s family.race_cd 1
execute if score @s family.race_cd matches 60 run title @s title {"text": "3", "color": "yellow", "bold": true}
execute if score @s family.race_cd matches 60 run playsound minecraft:block.note_block.pling master @s ~ ~ ~ 1 1
execute if score @s family.race_cd matches 40 run title @s title {"text": "2", "color": "yellow", "bold": true}
execute if score @s family.race_cd matches 40 run playsound minecraft:block.note_block.pling master @s ~ ~ ~ 1 1
execute if score @s family.race_cd matches 20 run title @s title {"text": "1", "color": "yellow", "bold": true}
execute if score @s family.race_cd matches 20 run playsound minecraft:block.note_block.pling master @s ~ ~ ~ 1 1
execute if score @s family.race_cd matches 0 run function family:undersea/race/go_now
