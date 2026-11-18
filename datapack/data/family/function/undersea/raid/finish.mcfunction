scoreboard players set #on family.raid 0
scoreboard players set #wave family.raid 0
scoreboard players set #cool family.raid 900
scoreboard players set #since family.raid 0
schedule clear family:undersea/raid/blink
execute as @e[tag=family.raider] at @s run function family:undersea/raid/flee
bossbar remove family:raid_wave
bossbar remove family:raid_spirit
bossbar remove family:raid_captain
kill @e[type=minecraft:text_display,tag=family.raid.banner]
function family:undersea/raid/lamps_white
execute as @a[tag=family.raid.in] run function family:undersea/raid/leave
