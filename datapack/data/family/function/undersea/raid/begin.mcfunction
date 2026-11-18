scoreboard players set #on family.raid 1
scoreboard players set #wave family.raid 0
scoreboard players operation #t family.raid = #warn family.raid
scoreboard players set #spirit family.raid 100
scoreboard players set #quiet family.raid 0
bossbar add family:raid_wave {"text":"ENEMY ATTACK!","color":"red"}
bossbar set family:raid_wave color red
execute store result bossbar family:raid_wave max run scoreboard players get #warn family.raid
execute store result bossbar family:raid_wave value run scoreboard players get #warn family.raid
bossbar add family:raid_spirit {"text":"Town Spirit","color":"green"}
bossbar set family:raid_spirit color green
bossbar set family:raid_spirit max 100
bossbar set family:raid_spirit value 100
execute in family:undersea run bossbar set family:raid_wave players @a[distance=0..]
execute in family:undersea run bossbar set family:raid_spirit players @a[distance=0..]
kill @e[type=minecraft:text_display,tag=family.raid.banner]
execute in family:undersea run summon minecraft:text_display -167.5 50.5 -155.5 {"Tags":["family.raid.banner"],"billboard":"center","brightness":{"sky":15,"block":15},"text":{"text":"ENEMY ATTACK!","color":"red","bold":true},"transformation":{"left_rotation":[0.0f,0.0f,0.0f,1.0f],"right_rotation":[0.0f,0.0f,0.0f,1.0f],"translation":[0.0f,0.0f,0.0f],"scale":[2.5f,2.5f,2.5f]}}
function family:undersea/raid/lamps_red
scoreboard players set #blink family.raid 0
schedule function family:undersea/raid/blink 10t replace
