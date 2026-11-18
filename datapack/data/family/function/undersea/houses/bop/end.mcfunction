scoreboard players set #c0 family.house 0
scoreboard players set #c1 family.house 0
scoreboard players set #c2 family.house 0
scoreboard players set #c3 family.house 0
scoreboard players set #c4 family.house 0
scoreboard players set #c5 family.house 0
scoreboard players set #c6 family.house 0
scoreboard players set #c7 family.house 0
function family:undersea/houses/bop/shut/0
function family:undersea/houses/bop/shut/1
function family:undersea/houses/bop/shut/2
function family:undersea/houses/bop/shut/3
function family:undersea/houses/bop/shut/4
function family:undersea/houses/bop/shut/5
function family:undersea/houses/bop/shut/6
function family:undersea/houses/bop/shut/7
execute in family:undersea as @a[x=-143,y=39,z=-167,dx=12,dy=11,dz=13] run tag @s add family.bopper
execute as @a[tag=family.bopper] at @s run function family:undersea/houses/bop/result
