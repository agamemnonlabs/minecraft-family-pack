schedule function family:undersea/alive/loop 1s replace
execute in family:undersea positioned -167.5 40 -143.5 if entity @a[distance=..32] run scoreboard players add #square family.alive 1
execute in family:undersea positioned -167.5 40 -143.5 unless entity @a[distance=..32] run scoreboard players set #square family.alive 0
execute if score #square family.alive matches 5.. run function family:undersea/alive/repair_square
execute in family:undersea positioned -167.5 42 -182.5 if entity @a[distance=..32] run scoreboard players add #meadow family.alive 1
execute in family:undersea positioned -167.5 42 -182.5 unless entity @a[distance=..32] run scoreboard players set #meadow family.alive 0
execute if score #meadow family.alive matches 5.. run function family:undersea/alive/repair_meadow
execute in family:undersea positioned -173.5 40 -137.5 as @e[type=minecraft:axolotl,tag=family.alive.noodle,distance=10..] run tp @s -173.5 40 -137.5
execute in family:undersea positioned -161.5 40 -149.5 as @e[type=minecraft:axolotl,tag=family.alive.sprinkles,distance=10..] run tp @s -161.5 40 -149.5
execute in family:undersea positioned -173.5 40 -149.5 as @e[type=minecraft:axolotl,tag=family.alive.puddle,distance=10..] run tp @s -173.5 40 -149.5
execute in family:undersea positioned -147.5 42 -174.5 as @e[type=minecraft:axolotl,tag=family.alive.blueberry,distance=8..] run tp @s -147.5 42 -174.5
execute in family:undersea positioned -173.5 46 -189.5 as @e[type=minecraft:glow_squid,tag=family.alive.glimmer,distance=8..] run tp @s -173.5 46 -189.5
execute in family:undersea positioned -159.5 46 -183.5 as @e[type=minecraft:glow_squid,tag=family.alive.twinkle,distance=8..] run tp @s -159.5 46 -183.5
execute in family:undersea positioned -155.5 47 -190.5 as @e[type=minecraft:glow_squid,tag=family.alive.lumo,distance=8..] run tp @s -155.5 47 -190.5
execute in family:undersea positioned -184.5 45 -179.5 as @e[type=minecraft:turtle,tag=family.alive.mossback,distance=6.5..] run tp @s -179.999 45 -179.52 0 0
execute in family:undersea positioned -172.5 44 -175.5 as @e[type=minecraft:turtle,tag=family.alive.pebble,distance=5.0..] run tp @s -169.5 44 -175.525 0 0
scoreboard players set #now family.alive -1
execute as @e[type=minecraft:villager,tag=family.folk.chef] run scoreboard players set #now family.alive 0
execute as @e[type=minecraft:villager,tag=family.folk.chef] if data entity @s sleeping_pos run scoreboard players set #now family.alive 1
execute as @e[type=minecraft:villager,tag=family.folk.chef] if data entity @s SleepingX run scoreboard players set #now family.alive 1
execute unless score #now family.alive matches -1 run scoreboard players operation #night family.alive = #now family.alive
execute if score #night family.alive matches 0 run function family:undersea/alive/day
execute if score #now family.alive matches 1 unless entity @e[type=minecraft:text_display,tag=family.alive.closed] run execute in family:undersea run summon minecraft:text_display -143.5 43.1 -135.5 {"Tags":["family.alive","family.alive.closed"],"billboard":"center","brightness":{"sky":15,"block":15},"text":[{"text":"CLOSED\n","color":"red","bold":true},{"text":"Chef Clamuel is asleep. Zzz\nOpen again at sunrise!","color":"white","bold":false}],"transformation":{"left_rotation":[0.0f,0.0f,0.0f,1.0f],"right_rotation":[0.0f,0.0f,0.0f,1.0f],"translation":[0.0f,0.0f,0.0f],"scale":[1.2f,1.2f,1.2f]}}
