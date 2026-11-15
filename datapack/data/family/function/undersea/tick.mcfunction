execute as @e[type=minecraft:marker,tag=family.portal] at @s run tag @a[distance=..1.5] add family.near_portal
execute as @a[tag=family.near_portal,tag=!family.in_portal] at @s run function family:undersea/portal
tag @a[tag=family.near_portal] add family.in_portal
tag @a[tag=!family.near_portal] remove family.in_portal
tag @a remove family.near_portal
