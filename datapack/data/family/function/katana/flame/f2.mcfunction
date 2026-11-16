tag @s add family.caster
particle minecraft:flame ^-0.75 ^-0.24 ^1.85 0.04 0.04 0.04 0.01 1
particle minecraft:flame ^-0.46 ^-0.16 ^1.95 0.04 0.04 0.04 0.01 1
particle minecraft:flame ^-0.15 ^-0.09 ^1.99 0.04 0.04 0.04 0.01 1
particle minecraft:flame ^0.15 ^-0.01 ^1.99 0.04 0.04 0.04 0.01 1
particle minecraft:flame ^0.46 ^0.06 ^1.95 0.04 0.04 0.04 0.01 1
particle minecraft:flame ^0.75 ^0.14 ^1.85 0.04 0.04 0.04 0.01 1
particle minecraft:dust{color:[1.00,0.35,0.12],scale:1.6} ^-0.86 ^-0.14 ^2.13 0.03 0.03 0.03 0.0 1
particle minecraft:dust{color:[1.00,0.35,0.12],scale:1.6} ^-0.53 ^-0.06 ^2.24 0.03 0.03 0.03 0.0 1
particle minecraft:dust{color:[1.00,0.35,0.12],scale:1.6} ^-0.18 ^0.01 ^2.29 0.03 0.03 0.03 0.0 1
particle minecraft:dust{color:[1.00,0.35,0.12],scale:1.6} ^0.18 ^0.09 ^2.29 0.03 0.03 0.03 0.0 1
particle minecraft:dust{color:[1.00,0.35,0.12],scale:1.6} ^0.53 ^0.16 ^2.24 0.03 0.03 0.03 0.0 1
particle minecraft:dust{color:[1.00,0.35,0.12],scale:1.6} ^0.86 ^0.24 ^2.13 0.03 0.03 0.03 0.0 1
execute positioned ^0 ^-1 ^1.8 as @e[type=#family:katana_targets,distance=..2.5] run damage @s 6 minecraft:player_attack by @p[tag=family.caster]
execute positioned ^0 ^-1 ^1.8 as @a[distance=..2.5,tag=!family.caster,gamemode=!spectator] run damage @s 0.01 family:katana_push by @p[tag=family.caster]
tag @s remove family.caster
