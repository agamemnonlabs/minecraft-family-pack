execute in family:undersea positioned -168 38 -144 unless loaded ~ ~ ~ run return run schedule function family:undersea/build_hub_2 2s replace
execute in family:undersea positioned -168 38 -144 run fill ~-6 ~1 ~-6 ~6 ~8 ~6 minecraft:water
execute in family:undersea positioned -168 38 -144 run fill ~-6 ~-1 ~-6 ~6 ~-1 ~6 minecraft:prismarine
execute in family:undersea positioned -168 38 -144 run fill ~-5 ~ ~-5 ~5 ~ ~5 minecraft:prismarine_bricks
execute in family:undersea positioned -168 38 -144 run setblock ~-5 ~ ~-5 minecraft:sea_lantern
execute in family:undersea positioned -168 38 -144 run setblock ~-5 ~ ~0 minecraft:sea_lantern
execute in family:undersea positioned -168 38 -144 run setblock ~-5 ~ ~5 minecraft:sea_lantern
execute in family:undersea positioned -168 38 -144 run setblock ~0 ~ ~-5 minecraft:sea_lantern
execute in family:undersea positioned -168 38 -144 run setblock ~0 ~ ~5 minecraft:sea_lantern
execute in family:undersea positioned -168 38 -144 run setblock ~5 ~ ~-5 minecraft:sea_lantern
execute in family:undersea positioned -168 38 -144 run setblock ~5 ~ ~0 minecraft:sea_lantern
execute in family:undersea positioned -168 38 -144 run setblock ~5 ~ ~5 minecraft:sea_lantern
execute in family:undersea positioned -168 38 -144 run setblock ~ ~ ~ minecraft:soul_sand
execute in family:undersea positioned -168 38 -144 run fill ~-2 ~1 ~-2 ~-2 ~3 ~-2 minecraft:dark_prismarine
execute in family:undersea positioned -168 38 -144 run fill ~-2 ~1 ~2 ~-2 ~3 ~2 minecraft:dark_prismarine
execute in family:undersea positioned -168 38 -144 run fill ~2 ~1 ~-2 ~2 ~3 ~-2 minecraft:dark_prismarine
execute in family:undersea positioned -168 38 -144 run fill ~2 ~1 ~2 ~2 ~3 ~2 minecraft:dark_prismarine
execute in family:undersea positioned -168 38 -144 run setblock ~-2 ~4 ~-2 minecraft:sea_lantern
execute in family:undersea positioned -168 38 -144 run setblock ~-2 ~4 ~2 minecraft:sea_lantern
execute in family:undersea positioned -168 38 -144 run setblock ~2 ~4 ~-2 minecraft:sea_lantern
execute in family:undersea positioned -168 38 -144 run setblock ~2 ~4 ~2 minecraft:sea_lantern
execute in family:undersea run kill @e[type=minecraft:marker,tag=family.portal_up,distance=0..]
execute in family:undersea positioned -168 38 -144 run summon minecraft:marker ~0.5 ~1.5 ~0.5 {Tags: ["family.portal", "family.portal_up"]}
data modify storage family:undersea hub set value {x: -167.5d, y: 39.0d, z: -140.5d}
execute in family:undersea run forceload remove -184 -160 -153 -129
