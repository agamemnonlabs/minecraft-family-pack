execute in family:undersea unless loaded -130 38 -152 run return run schedule function family:undersea/houses/build 2s replace
execute in family:undersea unless loaded -194 38 -169 run return run schedule function family:undersea/houses/build 2s replace
kill @e[type=minecraft:villager,tag=family.folk.professor]
kill @e[type=minecraft:villager,tag=family.folk.coach]
kill @e[type=minecraft:interaction,tag=family.tap.professor]
kill @e[type=minecraft:interaction,tag=family.tap.coach]
kill @e[tag=family.house]
execute in family:undersea positioned -168 38 -144 run summon minecraft:villager ~16 ~1 ~-21 {"Tags":["family.folk","family.folk.professor"],"CustomName":{"text":"Professor Periwinkle","color":"dark_aqua"},"CustomNameVisible":true,"Invulnerable":true,"PersistenceRequired":true,"Rotation":[0.0f,0.0f],"VillagerData":{"profession":"minecraft:librarian","level":5,"type":"minecraft:plains"},"Xp":250,"Offers":{"Recipes":[]},"NoAI":true}
execute in family:undersea positioned -168 38 -144 run summon minecraft:villager ~31 ~3 ~-21 {"Tags":["family.folk","family.folk.coach"],"CustomName":{"text":"Coach Cockle","color":"red"},"CustomNameVisible":true,"Invulnerable":true,"PersistenceRequired":true,"Rotation":[0.0f,0.0f],"VillagerData":{"profession":"minecraft:fisherman","level":5,"type":"minecraft:jungle"},"Xp":250,"Offers":{"Recipes":[]},"NoAI":true}
execute in family:undersea positioned -168 38 -144 run summon minecraft:interaction ~16 ~1.0 ~-21 {"Tags":["family.folk.box","family.tap.professor"],"width":1.0f,"height":2.2f}
execute in family:undersea positioned -168 38 -144 run summon minecraft:interaction ~31 ~3.0 ~-21 {"Tags":["family.folk.box","family.tap.coach"],"width":1.0f,"height":2.2f}
execute in family:undersea if block -140 40 -162 minecraft:water run setblock -140 40 -162 minecraft:bone_block[axis=y]
execute in family:undersea if block -139 40 -163 minecraft:water run setblock -139 40 -163 minecraft:bone_block[axis=y]
execute in family:undersea if block -135 40 -163 minecraft:water run setblock -135 40 -163 minecraft:bone_block[axis=y]
execute in family:undersea if block -134 40 -162 minecraft:water run setblock -134 40 -162 minecraft:bone_block[axis=y]
execute in family:undersea if block -134 40 -160 minecraft:water run setblock -134 40 -160 minecraft:bone_block[axis=y]
execute in family:undersea if block -135 40 -159 minecraft:water run setblock -135 40 -159 minecraft:bone_block[axis=y]
execute in family:undersea if block -139 40 -159 minecraft:water run setblock -139 40 -159 minecraft:bone_block[axis=y]
execute in family:undersea if block -140 40 -160 minecraft:water run setblock -140 40 -160 minecraft:bone_block[axis=y]
execute in family:undersea if block -140 40 -162 minecraft:pearlescent_froglight run setblock -140 40 -162 minecraft:bone_block[axis=y]
execute in family:undersea if block -139 40 -163 minecraft:pearlescent_froglight run setblock -139 40 -163 minecraft:bone_block[axis=y]
execute in family:undersea if block -135 40 -163 minecraft:pearlescent_froglight run setblock -135 40 -163 minecraft:bone_block[axis=y]
execute in family:undersea if block -134 40 -162 minecraft:pearlescent_froglight run setblock -134 40 -162 minecraft:bone_block[axis=y]
execute in family:undersea if block -134 40 -160 minecraft:pearlescent_froglight run setblock -134 40 -160 minecraft:bone_block[axis=y]
execute in family:undersea if block -135 40 -159 minecraft:pearlescent_froglight run setblock -135 40 -159 minecraft:bone_block[axis=y]
execute in family:undersea if block -139 40 -159 minecraft:pearlescent_froglight run setblock -139 40 -159 minecraft:bone_block[axis=y]
execute in family:undersea if block -140 40 -160 minecraft:pearlescent_froglight run setblock -140 40 -160 minecraft:bone_block[axis=y]
execute in family:undersea positioned -168 38 -144 run summon minecraft:interaction ~28 ~1.95 ~-18 {"Tags":["family.house","family.house.clam","family.tap.clam0"],"width":1.1f,"height":1.1f}
execute in family:undersea positioned -168 38 -144 run summon minecraft:interaction ~29 ~1.95 ~-19 {"Tags":["family.house","family.house.clam","family.tap.clam1"],"width":1.1f,"height":1.1f}
execute in family:undersea positioned -168 38 -144 run summon minecraft:interaction ~33 ~1.95 ~-19 {"Tags":["family.house","family.house.clam","family.tap.clam2"],"width":1.1f,"height":1.1f}
execute in family:undersea positioned -168 38 -144 run summon minecraft:interaction ~34 ~1.95 ~-18 {"Tags":["family.house","family.house.clam","family.tap.clam3"],"width":1.1f,"height":1.1f}
execute in family:undersea positioned -168 38 -144 run summon minecraft:interaction ~34 ~1.95 ~-16 {"Tags":["family.house","family.house.clam","family.tap.clam4"],"width":1.1f,"height":1.1f}
execute in family:undersea positioned -168 38 -144 run summon minecraft:interaction ~33 ~1.95 ~-15 {"Tags":["family.house","family.house.clam","family.tap.clam5"],"width":1.1f,"height":1.1f}
execute in family:undersea positioned -168 38 -144 run summon minecraft:interaction ~29 ~1.95 ~-15 {"Tags":["family.house","family.house.clam","family.tap.clam6"],"width":1.1f,"height":1.1f}
execute in family:undersea positioned -168 38 -144 run summon minecraft:interaction ~28 ~1.95 ~-16 {"Tags":["family.house","family.house.clam","family.tap.clam7"],"width":1.1f,"height":1.1f}
function family:undersea/houses/bop/board
execute in family:undersea if block -155 39 -165 minecraft:water run setblock -155 39 -165 minecraft:bookshelf
execute in family:undersea if block -154 39 -165 minecraft:water run setblock -154 39 -165 minecraft:bookshelf
execute in family:undersea if block -150 39 -165 minecraft:water run setblock -150 39 -165 minecraft:bookshelf
execute in family:undersea if block -149 39 -165 minecraft:water run setblock -149 39 -165 minecraft:bookshelf
execute in family:undersea if block -154 40 -165 minecraft:water run setblock -154 40 -165 minecraft:bookshelf
execute in family:undersea if block -150 40 -165 minecraft:water run setblock -150 40 -165 minecraft:bookshelf
execute in family:undersea if block -152 39 -166 minecraft:water run setblock -152 39 -166 minecraft:bookshelf
execute in family:undersea if block -154 39 -164 minecraft:water run setblock -154 39 -164 minecraft:lectern[facing=south]
execute in family:undersea if block -184 43 -153 minecraft:water run setblock -184 43 -153 minecraft:oak_wall_sign[waterlogged=true,facing=south]{front_text:{messages:[{text:"~ Clubhouse ~"},{text:""},{text:"(name me!)"},{text:""}]}}
execute in family:undersea if block -152 43 -155 minecraft:water run setblock -152 43 -155 minecraft:oak_wall_sign[waterlogged=true,facing=south]{front_text:{messages:[{text:"Professor"},{text:"Periwinkle"},{text:"Jokes, facts"},{text:"and riddles!"}]}}
execute in family:undersea if block -137 43 -154 minecraft:water run setblock -137 43 -154 minecraft:oak_wall_sign[waterlogged=true,facing=south]{front_text:{messages:[{text:"~ Clam Bop ~"},{text:""},{text:"Tap the Coach"},{text:"to play!"}]}}
function family:undersea/houses/club
scoreboard players set #built family.house 1
execute in family:undersea run forceload remove -194 -169 -130 -152
