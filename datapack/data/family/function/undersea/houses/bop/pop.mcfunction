execute store result score #pick family.house run random value 0..7
execute if score #pick family.house matches 0 run function family:undersea/houses/bop/open/0
execute if score #pick family.house matches 1 run function family:undersea/houses/bop/open/1
execute if score #pick family.house matches 2 run function family:undersea/houses/bop/open/2
execute if score #pick family.house matches 3 run function family:undersea/houses/bop/open/3
execute if score #pick family.house matches 4 run function family:undersea/houses/bop/open/4
execute if score #pick family.house matches 5 run function family:undersea/houses/bop/open/5
execute if score #pick family.house matches 6 run function family:undersea/houses/bop/open/6
execute if score #pick family.house matches 7 run function family:undersea/houses/bop/open/7
execute if score #game family.house matches 401..600 store result score #next family.house run random value 12..20
execute if score #game family.house matches 201..400 store result score #next family.house run random value 9..15
execute if score #game family.house matches 1..200 store result score #next family.house run random value 6..11
