fill ~-2 ~-3 ~-2 ~2 ~-1 ~2 minecraft:prismarine_bricks
fill ~-1 ~-2 ~-1 ~1 ~-1 ~1 minecraft:water
setblock ~ ~-3 ~ minecraft:soul_sand
setblock ~-2 ~-1 ~-2 minecraft:sea_lantern
setblock ~-2 ~-1 ~2 minecraft:sea_lantern
setblock ~2 ~-1 ~-2 minecraft:sea_lantern
setblock ~2 ~-1 ~2 minecraft:sea_lantern
summon minecraft:marker ~ ~-1.5 ~ {Tags: ["family.portal", "family.portal_down"]}
summon minecraft:marker ~ ~ ~2 {Tags: ["family.tmp"]}
execute store result storage family:undersea home.x double 0.01 run data get entity @n[type=minecraft:marker,tag=family.tmp] Pos[0] 100
execute store result storage family:undersea home.y double 0.01 run data get entity @n[type=minecraft:marker,tag=family.tmp] Pos[1] 100
execute store result storage family:undersea home.z double 0.01 run data get entity @n[type=minecraft:marker,tag=family.tmp] Pos[2] 100
kill @e[type=minecraft:marker,tag=family.tmp]
tp @s ~ ~ ~2
tellraw @s {"text": "Undersea whirlpool built. Jump in!", "color": "aqua"}
