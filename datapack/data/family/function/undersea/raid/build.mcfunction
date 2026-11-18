execute in family:undersea unless loaded -168 38 -148 run return run schedule function family:undersea/raid/build 2s replace
execute in family:undersea unless loaded -174 38 -156 run return run schedule function family:undersea/raid/build 2s replace
execute in family:undersea run kill @e[tag=family.raid.alarm]
execute in family:undersea if block -174 39 -156 minecraft:prismarine_wall run setblock -174 39 -156 minecraft:water
execute in family:undersea if block -174 40 -156 minecraft:prismarine_wall run setblock -174 40 -156 minecraft:water
execute in family:undersea if block -174 41 -156 minecraft:bell run setblock -174 41 -156 minecraft:water
execute in family:undersea if block -168 39 -148 #family:race_free run setblock -168 39 -148 minecraft:prismarine_wall[waterlogged=true]
execute in family:undersea if block -168 40 -148 #family:race_free run setblock -168 40 -148 minecraft:prismarine_wall[waterlogged=true]
execute in family:undersea if block -168 41 -148 #family:race_free run setblock -168 41 -148 minecraft:bell[attachment=floor,facing=south]
execute in family:undersea run summon minecraft:interaction -167.5 38.95 -147.5 {"Tags":["family.raid.alarm","family.tap.alarm"],"width":1.2f,"height":3.3f}
execute in family:undersea run summon minecraft:text_display -167.5 42.6 -147.5 {"Tags":["family.raid.alarm","family.raid.label"],"billboard":"center","brightness":{"sky":15,"block":15},"transformation":{"left_rotation":[0.0f,0.0f,0.0f,1.0f],"right_rotation":[0.0f,0.0f,0.0f,1.0f],"translation":[0.0f,0.0f,0.0f],"scale":[1.6f,1.6f,1.6f]},"text":[{"text":"ALARM BELL\n","color":"red","bold":true},{"text":"Tap to call the sea raiders!","color":"white","bold":false}]}
scoreboard players set #built family.raid 1
execute in family:undersea run forceload remove -175 -157 -167 -147
