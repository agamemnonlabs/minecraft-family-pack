schedule function family:undersea/houses/loop 1s replace
execute in family:undersea positioned -136.5 42.5 -160.5 if entity @a[distance=..20] run scoreboard players add #near family.house 1
execute in family:undersea positioned -136.5 42.5 -160.5 unless entity @a[distance=..20] run scoreboard players set #near family.house 0
execute if score #built family.house matches 1 if score #near family.house matches 5.. run function family:undersea/houses/repair
