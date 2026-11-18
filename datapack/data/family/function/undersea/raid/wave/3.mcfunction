scoreboard players set #wave family.raid 3
scoreboard players set #t family.raid 0
execute store result score #n family.raid if entity @a[tag=family.raid.in]
execute if score #n family.raid matches ..0 run scoreboard players set #n family.raid 1
execute store result score #alive family.raid if entity @e[tag=family.raider,tag=!family.raid.mount]
execute in family:undersea positioned -167.5 38 -209.5 positioned over ocean_floor run summon minecraft:drowned ~ ~ ~ {"Tags":["family.raider","family.raid.new","family.raid.captain"],"Team":"family.raiders","CustomName":{"text":"Captain Grimtide","color":"light_purple"},"Health":60.0f,"CanPickUpLoot":false,"PersistenceRequired":true,"DeathLootTable":"family:raid/captain","drop_chances":{"mainhand":0.0f,"head":0.0f},"attributes":[{"id":"minecraft:max_health","base":60.0},{"id":"minecraft:follow_range","base":64.0},{"id":"minecraft:attack_damage","base":2.0},{"id":"minecraft:scale","base":1.8},{"id":"minecraft:knockback_resistance","base":0.6}],"equipment":{"mainhand":{"id":"minecraft:spyglass","count":1},"head":{"id":"minecraft:golden_helmet","count":1}},"CustomNameVisible":true}
function family:undersea/raid/settle
execute in family:undersea positioned -167.5 38 -209.5 positioned over ocean_floor run particle minecraft:sonic_boom ~ ~2 ~ 1 1 1 0 3 force
execute in family:undersea positioned -167.5 38 -209.5 positioned over ocean_floor run particle minecraft:explosion_emitter ~ ~2 ~ 0 0 0 0 1 force
bossbar add family:raid_captain {"text":"Captain Grimtide","color":"light_purple"}
bossbar set family:raid_captain color purple
bossbar set family:raid_captain max 60
bossbar set family:raid_captain value 60
scoreboard players operation #k family.raid = #n family.raid
scoreboard players add #k family.raid 2
function family:undersea/raid/many/rider/n
function family:undersea/raid/whirl/n
execute store result score #left family.raid if entity @e[tag=family.raider,tag=!family.raid.mount]
execute store result bossbar family:raid_wave max run scoreboard players get #left family.raid
execute in family:undersea as @a[distance=0..] at @s run function family:undersea/raid/fx/wave3
execute in family:undersea run tellraw @a[distance=0..] [{"text": "Mayor Marina", "color": "light_purple"}, {"text": ": That's Captain Grimtide! Beat him and the rest will swim away!", "color": "white"}]
