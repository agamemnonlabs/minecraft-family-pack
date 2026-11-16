tag @s add family.caster
particle minecraft:electric_spark ^-0.35 ^-1.50 ^1.50 0.1 0.1 0.1 0.05 3
particle minecraft:electric_spark ^0.35 ^-1.50 ^1.90 0.1 0.1 0.1 0.05 3
particle minecraft:electric_spark ^-0.35 ^-1.50 ^2.30 0.1 0.1 0.1 0.05 3
particle minecraft:electric_spark ^0.35 ^-1.50 ^2.70 0.1 0.1 0.1 0.05 3
particle minecraft:electric_spark ^-0.35 ^-1.50 ^3.10 0.1 0.1 0.1 0.05 3
particle minecraft:electric_spark ^0.35 ^-1.50 ^3.50 0.1 0.1 0.1 0.05 3
particle minecraft:electric_spark ^-0.35 ^-1.50 ^3.90 0.1 0.1 0.1 0.05 3
particle minecraft:electric_spark ^0.35 ^-1.50 ^4.30 0.1 0.1 0.1 0.05 3
particle minecraft:electric_spark ^-0.35 ^-1.50 ^4.70 0.1 0.1 0.1 0.05 3
particle minecraft:dust{color:[1.00,0.96,0.60],scale:1.5} ^-0.35 ^-1.50 ^1.50 0.03 0.03 0.03 0.0 1
particle minecraft:dust{color:[1.00,0.96,0.60],scale:1.5} ^0.35 ^-1.50 ^1.90 0.03 0.03 0.03 0.0 1
particle minecraft:dust{color:[1.00,0.96,0.60],scale:1.5} ^-0.35 ^-1.50 ^2.30 0.03 0.03 0.03 0.0 1
particle minecraft:dust{color:[1.00,0.96,0.60],scale:1.5} ^0.35 ^-1.50 ^2.70 0.03 0.03 0.03 0.0 1
particle minecraft:dust{color:[1.00,0.96,0.60],scale:1.5} ^-0.35 ^-1.50 ^3.10 0.03 0.03 0.03 0.0 1
particle minecraft:dust{color:[1.00,0.96,0.60],scale:1.5} ^0.35 ^-1.50 ^3.50 0.03 0.03 0.03 0.0 1
particle minecraft:dust{color:[1.00,0.96,0.60],scale:1.5} ^-0.35 ^-1.50 ^3.90 0.03 0.03 0.03 0.0 1
particle minecraft:dust{color:[1.00,0.96,0.60],scale:1.5} ^0.35 ^-1.50 ^4.30 0.03 0.03 0.03 0.0 1
particle minecraft:dust{color:[1.00,0.96,0.60],scale:1.5} ^-0.35 ^-1.50 ^4.70 0.03 0.03 0.03 0.0 1
particle minecraft:firework ^-0.35 ^-1.50 ^4.70 0.2 0.2 0.2 0.05 6
execute positioned ^0 ^-1.1 ^2.6 as @e[type=#family:katana_targets,distance=..2.4] run damage @s 6 minecraft:player_attack by @p[tag=family.caster]
execute positioned ^0 ^-1.1 ^2.6 as @a[distance=..2.4,tag=!family.caster,gamemode=!spectator] run damage @s 0.01 family:katana_push by @p[tag=family.caster]
tag @s remove family.caster
