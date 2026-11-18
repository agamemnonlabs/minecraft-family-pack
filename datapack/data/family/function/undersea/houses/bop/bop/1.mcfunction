execute unless score #game family.house matches 1..600 run return fail
execute unless score #c1 family.house matches 1.. run return fail
scoreboard players set #c1 family.house 0
function family:undersea/houses/bop/shut/1
scoreboard players add @s family.bops 1
tag @s add family.bopper
execute in family:undersea run particle minecraft:end_rod -138.5 40.5 -162.5 0.3 0.3 0.3 0.05 10
playsound minecraft:entity.experience_orb.pickup master @s ~ ~ ~ 1 1.2
