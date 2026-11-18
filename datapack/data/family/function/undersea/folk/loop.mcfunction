schedule function family:undersea/folk/loop 5t replace
execute as @a[scores={family.talk=1..}] run function family:undersea/folk/button
execute as @e[type=minecraft:villager,tag=family.folk.chef] at @s as @a[distance=..5,tag=!family.met.chef] run function family:undersea/folk/hello/chef
execute as @e[type=minecraft:villager,tag=family.folk.chef] at @s run tag @a[distance=12..,tag=family.met.chef] remove family.met.chef
execute as @e[type=minecraft:villager,tag=family.folk.mayor] at @s as @a[distance=..5,tag=!family.met.mayor] run function family:undersea/folk/hello/mayor
execute as @e[type=minecraft:villager,tag=family.folk.mayor] at @s run tag @a[distance=12..,tag=family.met.mayor] remove family.met.mayor
execute as @e[type=minecraft:villager,tag=family.folk.farmer] at @s as @a[distance=..5,tag=!family.met.farmer] run function family:undersea/folk/hello/farmer
execute as @e[type=minecraft:villager,tag=family.folk.farmer] at @s run tag @a[distance=12..,tag=family.met.farmer] remove family.met.farmer
execute as @e[type=minecraft:villager,tag=family.folk.driver] at @s as @a[distance=..5,tag=!family.met.driver] run function family:undersea/folk/hello/driver
execute as @e[type=minecraft:villager,tag=family.folk.driver] at @s run tag @a[distance=12..,tag=family.met.driver] remove family.met.driver
execute as @e[type=minecraft:villager,tag=family.folk.professor] at @s as @a[distance=..5,tag=!family.met.professor] run function family:undersea/folk/hello/professor
execute as @e[type=minecraft:villager,tag=family.folk.professor] at @s run tag @a[distance=12..,tag=family.met.professor] remove family.met.professor
execute as @e[type=minecraft:villager,tag=family.folk.coach] at @s as @a[distance=..5,tag=!family.met.coach] run function family:undersea/folk/hello/coach
execute as @e[type=minecraft:villager,tag=family.folk.coach] at @s run tag @a[distance=12..,tag=family.met.coach] remove family.met.coach
execute as @e[type=minecraft:villager,tag=family.folk.mayor] at @s if entity @a[distance=..8] run rotate @s facing entity @p eyes
execute as @e[type=minecraft:villager,tag=family.folk.mayor] at @s unless entity @a[distance=..8] run rotate @s 0 0
execute as @e[type=minecraft:villager,tag=family.folk.farmer] at @s if entity @a[distance=..8] run rotate @s facing entity @p eyes
execute as @e[type=minecraft:villager,tag=family.folk.farmer] at @s unless entity @a[distance=..8] run rotate @s 0 0
execute as @e[type=minecraft:villager,tag=family.folk.driver] at @s if entity @a[distance=..8] run rotate @s facing entity @p eyes
execute as @e[type=minecraft:villager,tag=family.folk.driver] at @s unless entity @a[distance=..8] run rotate @s 90 0
execute as @e[type=minecraft:villager,tag=family.folk.professor] at @s if entity @a[distance=..8] run rotate @s facing entity @p eyes
execute as @e[type=minecraft:villager,tag=family.folk.professor] at @s unless entity @a[distance=..8] run rotate @s 0 0
execute as @e[type=minecraft:villager,tag=family.folk.coach] at @s if entity @a[distance=..8] run rotate @s facing entity @p eyes
execute as @e[type=minecraft:villager,tag=family.folk.coach] at @s unless entity @a[distance=..8] run rotate @s 0 0
execute in family:undersea as @e[type=minecraft:villager,tag=family.folk.chef] unless entity @s[x=-136,y=40,z=-133,dx=1,dy=1,dz=4] run tp @s -135.5 40 -130.5
execute in family:undersea positioned -168 38 -144 if entity @a[distance=..24] run scoreboard players add #near family.folk 5
execute in family:undersea positioned -168 38 -144 unless entity @a[distance=..24] run scoreboard players set #near family.folk 0
execute if score #near family.folk matches 100.. run function family:undersea/folk/repair
