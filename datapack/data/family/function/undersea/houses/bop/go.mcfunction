scoreboard players reset * family.bops
tag @a remove family.bopper
execute as @e[type=minecraft:interaction,tag=family.house.clam] run data remove entity @s attack
scoreboard players set #next family.house 6
execute in family:undersea as @a[x=-143,y=39,z=-167,dx=12,dy=11,dz=13] run title @s subtitle {"text":"Bop the pink clams!","color":"light_purple"}
execute in family:undersea as @a[x=-143,y=39,z=-167,dx=12,dy=11,dz=13] run title @s title {"text":"GO!","color":"green","bold":true}
execute in family:undersea as @a[x=-143,y=39,z=-167,dx=12,dy=11,dz=13] at @s run playsound minecraft:block.note_block.pling master @s ~ ~ ~ 1 2
