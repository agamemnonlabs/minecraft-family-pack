tag @s add family.chute_open
tag @s remove family.chute_folded
item modify entity @s armor.chest family:parachute/open
effect give @s minecraft:slow_falling 2 0 true
playsound minecraft:family.parachute_open player @a ~ ~ ~ 1 1
summon minecraft:item_display ~ ~1.8 ~ {Tags:["family.canopy","family.canopy_new","family.canopy_grow"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"family:parachute_canopy"}},item_display:"none",transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,-0.2f,0f],scale:[0.3f,0.3f,0.3f]}}
tag @s add family.chute_mount
title @s actionbar {"text": "Parachute open! Crouch to fold it.", "color": "#FF9A3C"}
