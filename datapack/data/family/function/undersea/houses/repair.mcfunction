scoreboard players set #near family.house 0
execute unless entity @e[type=minecraft:interaction,tag=family.tap.clam0] run execute in family:undersea positioned -168 38 -144 run summon minecraft:interaction ~28 ~1.95 ~-18 {"Tags":["family.house","family.house.clam","family.tap.clam0"],"width":1.1f,"height":1.1f}
execute unless entity @e[type=minecraft:interaction,tag=family.tap.clam1] run execute in family:undersea positioned -168 38 -144 run summon minecraft:interaction ~29 ~1.95 ~-19 {"Tags":["family.house","family.house.clam","family.tap.clam1"],"width":1.1f,"height":1.1f}
execute unless entity @e[type=minecraft:interaction,tag=family.tap.clam2] run execute in family:undersea positioned -168 38 -144 run summon minecraft:interaction ~33 ~1.95 ~-19 {"Tags":["family.house","family.house.clam","family.tap.clam2"],"width":1.1f,"height":1.1f}
execute unless entity @e[type=minecraft:interaction,tag=family.tap.clam3] run execute in family:undersea positioned -168 38 -144 run summon minecraft:interaction ~34 ~1.95 ~-18 {"Tags":["family.house","family.house.clam","family.tap.clam3"],"width":1.1f,"height":1.1f}
execute unless entity @e[type=minecraft:interaction,tag=family.tap.clam4] run execute in family:undersea positioned -168 38 -144 run summon minecraft:interaction ~34 ~1.95 ~-16 {"Tags":["family.house","family.house.clam","family.tap.clam4"],"width":1.1f,"height":1.1f}
execute unless entity @e[type=minecraft:interaction,tag=family.tap.clam5] run execute in family:undersea positioned -168 38 -144 run summon minecraft:interaction ~33 ~1.95 ~-15 {"Tags":["family.house","family.house.clam","family.tap.clam5"],"width":1.1f,"height":1.1f}
execute unless entity @e[type=minecraft:interaction,tag=family.tap.clam6] run execute in family:undersea positioned -168 38 -144 run summon minecraft:interaction ~29 ~1.95 ~-15 {"Tags":["family.house","family.house.clam","family.tap.clam6"],"width":1.1f,"height":1.1f}
execute unless entity @e[type=minecraft:interaction,tag=family.tap.clam7] run execute in family:undersea positioned -168 38 -144 run summon minecraft:interaction ~28 ~1.95 ~-16 {"Tags":["family.house","family.house.clam","family.tap.clam7"],"width":1.1f,"height":1.1f}
execute unless entity @e[type=minecraft:text_display,tag=family.house.board] run function family:undersea/houses/bop/board
execute if score #game family.house matches 1.. run return 0
execute in family:undersea if block -140 40 -162 minecraft:pearlescent_froglight run setblock -140 40 -162 minecraft:bone_block[axis=y]
execute in family:undersea if block -140 40 -162 minecraft:water run setblock -140 40 -162 minecraft:bone_block[axis=y]
execute in family:undersea if block -139 40 -163 minecraft:pearlescent_froglight run setblock -139 40 -163 minecraft:bone_block[axis=y]
execute in family:undersea if block -139 40 -163 minecraft:water run setblock -139 40 -163 minecraft:bone_block[axis=y]
execute in family:undersea if block -135 40 -163 minecraft:pearlescent_froglight run setblock -135 40 -163 minecraft:bone_block[axis=y]
execute in family:undersea if block -135 40 -163 minecraft:water run setblock -135 40 -163 minecraft:bone_block[axis=y]
execute in family:undersea if block -134 40 -162 minecraft:pearlescent_froglight run setblock -134 40 -162 minecraft:bone_block[axis=y]
execute in family:undersea if block -134 40 -162 minecraft:water run setblock -134 40 -162 minecraft:bone_block[axis=y]
execute in family:undersea if block -134 40 -160 minecraft:pearlescent_froglight run setblock -134 40 -160 minecraft:bone_block[axis=y]
execute in family:undersea if block -134 40 -160 minecraft:water run setblock -134 40 -160 minecraft:bone_block[axis=y]
execute in family:undersea if block -135 40 -159 minecraft:pearlescent_froglight run setblock -135 40 -159 minecraft:bone_block[axis=y]
execute in family:undersea if block -135 40 -159 minecraft:water run setblock -135 40 -159 minecraft:bone_block[axis=y]
execute in family:undersea if block -139 40 -159 minecraft:pearlescent_froglight run setblock -139 40 -159 minecraft:bone_block[axis=y]
execute in family:undersea if block -139 40 -159 minecraft:water run setblock -139 40 -159 minecraft:bone_block[axis=y]
execute in family:undersea if block -140 40 -160 minecraft:pearlescent_froglight run setblock -140 40 -160 minecraft:bone_block[axis=y]
execute in family:undersea if block -140 40 -160 minecraft:water run setblock -140 40 -160 minecraft:bone_block[axis=y]
