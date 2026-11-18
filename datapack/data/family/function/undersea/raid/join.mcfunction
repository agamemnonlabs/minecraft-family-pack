tag @s add family.raid.in
execute if entity @s[gamemode=creative] run tag @s add family.raid.creative
execute if entity @s[gamemode=survival] run tag @s add family.raid.survival
gamemode adventure @s
tellraw @s {"text":"You're in the fight! No flying until the raid is over. If you get hurt, a bubble carries you to safety.","color":"gold"}
