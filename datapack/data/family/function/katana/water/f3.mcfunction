tag @s add family.caster
particle minecraft:dust{color:[0.25,0.66,1.00],scale:1.4} ^0.13 ^-0.64 ^2.00 0.03 0.03 0.03 0.0 1
particle minecraft:dust{color:[0.25,0.66,1.00],scale:1.4} ^0.38 ^-0.60 ^1.96 0.03 0.03 0.03 0.0 1
particle minecraft:dust{color:[0.25,0.66,1.00],scale:1.4} ^0.63 ^-0.53 ^1.90 0.03 0.03 0.03 0.0 1
particle minecraft:dust{color:[0.25,0.66,1.00],scale:1.4} ^0.87 ^-0.43 ^1.80 0.03 0.03 0.03 0.0 1
particle minecraft:dust{color:[0.25,0.66,1.00],scale:1.4} ^1.10 ^-0.33 ^1.67 0.03 0.03 0.03 0.0 1
particle minecraft:dust{color:[0.25,0.66,1.00],scale:1.4} ^1.30 ^-0.24 ^1.52 0.03 0.03 0.03 0.0 1
particle minecraft:dust{color:[0.78,0.96,1.00],scale:1.0} ^0.15 ^-0.16 ^2.35 0.03 0.03 0.03 0.0 1
particle minecraft:dust{color:[0.78,0.96,1.00],scale:1.0} ^0.45 ^-0.20 ^2.31 0.03 0.03 0.03 0.0 1
particle minecraft:dust{color:[0.78,0.96,1.00],scale:1.0} ^0.74 ^-0.27 ^2.23 0.03 0.03 0.03 0.0 1
particle minecraft:dust{color:[0.78,0.96,1.00],scale:1.0} ^1.03 ^-0.37 ^2.11 0.03 0.03 0.03 0.0 1
particle minecraft:dust{color:[0.78,0.96,1.00],scale:1.0} ^1.29 ^-0.47 ^1.97 0.03 0.03 0.03 0.0 1
particle minecraft:dust{color:[0.78,0.96,1.00],scale:1.0} ^1.53 ^-0.56 ^1.78 0.03 0.03 0.03 0.0 1
particle minecraft:splash ^0.13 ^-0.64 ^2.00 0.1 0.1 0.1 0 2
particle minecraft:splash ^0.63 ^-0.53 ^1.90 0.1 0.1 0.1 0 2
particle minecraft:splash ^1.10 ^-0.33 ^1.67 0.1 0.1 0.1 0 2
execute positioned ^0 ^-1 ^1.8 as @e[type=#family:katana_targets,distance=..2.6] run damage @s 6 minecraft:player_attack by @p[tag=family.caster]
execute positioned ^0 ^-1 ^1.8 as @a[distance=..2.6,tag=!family.caster,gamemode=!spectator] run damage @s 0.01 family:katana_push by @p[tag=family.caster]
tag @s remove family.caster
