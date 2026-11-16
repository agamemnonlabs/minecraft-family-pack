tag @s add family.caster
particle minecraft:dust{color:[0.92,1.00,0.96],scale:1.2} ^-0.65 ^-0.45 ^3.28 0.03 0.03 0.03 0.0 1
particle minecraft:dust{color:[0.92,1.00,0.96],scale:1.2} ^-0.42 ^-0.80 ^3.43 0.03 0.03 0.03 0.0 1
particle minecraft:dust{color:[0.92,1.00,0.96],scale:1.2} ^-0.04 ^-0.96 ^3.59 0.03 0.03 0.03 0.0 1
particle minecraft:dust{color:[0.92,1.00,0.96],scale:1.2} ^0.38 ^-0.86 ^3.74 0.03 0.03 0.03 0.0 1
particle minecraft:dust{color:[0.92,1.00,0.96],scale:1.2} ^0.68 ^-0.54 ^3.90 0.03 0.03 0.03 0.0 1
particle minecraft:dust{color:[0.92,1.00,0.96],scale:1.2} ^0.74 ^-0.10 ^4.05 0.03 0.03 0.03 0.0 1
particle minecraft:dust{color:[0.92,1.00,0.96],scale:1.2} ^0.53 ^0.31 ^4.21 0.03 0.03 0.03 0.0 1
particle minecraft:dust{color:[0.92,1.00,0.96],scale:1.2} ^0.12 ^0.53 ^4.36 0.03 0.03 0.03 0.0 1
particle minecraft:dust{color:[0.44,0.95,0.75],scale:1.0} ^0.65 ^-0.05 ^3.28 0.03 0.03 0.03 0.0 1
particle minecraft:dust{color:[0.44,0.95,0.75],scale:1.0} ^0.42 ^0.30 ^3.43 0.03 0.03 0.03 0.0 1
particle minecraft:dust{color:[0.44,0.95,0.75],scale:1.0} ^0.04 ^0.46 ^3.59 0.03 0.03 0.03 0.0 1
particle minecraft:dust{color:[0.44,0.95,0.75],scale:1.0} ^-0.38 ^0.36 ^3.74 0.03 0.03 0.03 0.0 1
particle minecraft:dust{color:[0.44,0.95,0.75],scale:1.0} ^-0.68 ^0.04 ^3.90 0.03 0.03 0.03 0.0 1
particle minecraft:dust{color:[0.44,0.95,0.75],scale:1.0} ^-0.74 ^-0.40 ^4.05 0.03 0.03 0.03 0.0 1
particle minecraft:dust{color:[0.44,0.95,0.75],scale:1.0} ^-0.53 ^-0.81 ^4.21 0.03 0.03 0.03 0.0 1
particle minecraft:dust{color:[0.44,0.95,0.75],scale:1.0} ^-0.12 ^-1.03 ^4.36 0.03 0.03 0.03 0.0 1
execute positioned ^0 ^-1 ^2.0 as @e[type=#family:katana_targets,distance=..1.7] run damage @s 6 minecraft:player_attack by @p[tag=family.caster]
execute positioned ^0 ^-1 ^2.0 as @a[distance=..1.7,tag=!family.caster,gamemode=!spectator] run damage @s 0.01 family:katana_push by @p[tag=family.caster]
execute positioned ^0 ^-1 ^4.0 as @e[type=#family:katana_targets,distance=..1.9] run damage @s 6 minecraft:player_attack by @p[tag=family.caster]
execute positioned ^0 ^-1 ^4.0 as @a[distance=..1.9,tag=!family.caster,gamemode=!spectator] run damage @s 0.01 family:katana_push by @p[tag=family.caster]
tag @s remove family.caster
