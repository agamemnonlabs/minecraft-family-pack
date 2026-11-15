execute in family:undersea unless loaded 0 86 0 run return run schedule function family:undersea/build_hub_2 2s replace
execute in family:undersea run fill -6 87 -6 6 94 6 minecraft:water
execute in family:undersea run fill -6 85 -6 6 85 6 minecraft:prismarine
execute in family:undersea run fill -5 86 -5 5 86 5 minecraft:prismarine_bricks
execute in family:undersea run setblock -5 86 -5 minecraft:sea_lantern
execute in family:undersea run setblock -5 86 0 minecraft:sea_lantern
execute in family:undersea run setblock -5 86 5 minecraft:sea_lantern
execute in family:undersea run setblock 0 86 -5 minecraft:sea_lantern
execute in family:undersea run setblock 0 86 5 minecraft:sea_lantern
execute in family:undersea run setblock 5 86 -5 minecraft:sea_lantern
execute in family:undersea run setblock 5 86 0 minecraft:sea_lantern
execute in family:undersea run setblock 5 86 5 minecraft:sea_lantern
execute in family:undersea run setblock 0 86 0 minecraft:soul_sand
execute in family:undersea run fill -2 87 -2 -2 89 -2 minecraft:dark_prismarine
execute in family:undersea run fill -2 87 2 -2 89 2 minecraft:dark_prismarine
execute in family:undersea run fill 2 87 -2 2 89 -2 minecraft:dark_prismarine
execute in family:undersea run fill 2 87 2 2 89 2 minecraft:dark_prismarine
execute in family:undersea run setblock -2 90 -2 minecraft:sea_lantern
execute in family:undersea run setblock -2 90 2 minecraft:sea_lantern
execute in family:undersea run setblock 2 90 -2 minecraft:sea_lantern
execute in family:undersea run setblock 2 90 2 minecraft:sea_lantern
execute in family:undersea run kill @e[type=minecraft:marker,tag=family.portal_up,distance=0..]
execute in family:undersea run summon minecraft:marker 0.5 87.5 0.5 {Tags: ["family.portal", "family.portal_up"]}
data modify storage family:undersea hub set value {x: 0.5d, y: 87.0d, z: 3.5d}
execute in family:undersea run forceload remove -16 -16 15 15
