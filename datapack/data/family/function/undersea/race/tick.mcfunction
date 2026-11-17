execute as @a[team=!family.undersea] at @s if dimension family:undersea run team join family.undersea @s
execute as @a[team=family.undersea] at @s unless dimension family:undersea run team leave @s
execute as @a[scores={family.race_left=1..}] run function family:undersea/race/rejoined
scoreboard players add #repair family.race_tmp 1
execute if score #repair family.race_tmp matches 100.. run function family:undersea/race/repair
execute unless entity @a[tag=family.racing] run return 0
scoreboard players add #spark family.race_tmp 1
execute if score #spark family.race_tmp matches 5.. run scoreboard players set #spark family.race_tmp 0
execute in family:undersea as @a[tag=family.racing,scores={family.race_cp=0,family.race_cd=0},x=-171,y=39,z=-126,dx=6,dy=6,dz=0] at @s run function family:undersea/race/started
execute in family:undersea as @a[tag=family.racing,scores={family.race_cp=1},x=-170,y=40,z=-121,dx=4,dy=4,dz=0] at @s run function family:undersea/race/cp/1
execute in family:undersea as @a[tag=family.racing,scores={family.race_cp=2},x=-153,y=41,z=-108,dx=0,dy=4,dz=4] at @s run function family:undersea/race/cp/2
execute in family:undersea as @a[tag=family.racing,scores={family.race_cp=3},x=-140,y=41,z=-108,dx=0,dy=4,dz=4] at @s run function family:undersea/race/cp/3
execute in family:undersea as @a[tag=family.racing,scores={family.race_cp=4},x=-128,y=41,z=-118,dx=4,dy=4,dz=0] at @s run function family:undersea/race/cp/4
execute in family:undersea as @a[tag=family.racing,scores={family.race_cp=5},x=-126,y=51,z=-146,dx=4,dy=0,dz=4] at @s run function family:undersea/race/cp/5
execute in family:undersea as @a[tag=family.racing,scores={family.race_cp=6},x=-128,y=43,z=-170,dx=4,dy=4,dz=0] at @s run function family:undersea/race/cp/6
execute in family:undersea as @a[tag=family.racing,scores={family.race_cp=7},x=-138,y=43,z=-184,dx=0,dy=4,dz=4] at @s run function family:undersea/race/cp/7
execute in family:undersea as @a[tag=family.racing,scores={family.race_cp=8},x=-156,y=44,z=-184,dx=0,dy=4,dz=4] at @s run function family:undersea/race/cp/8
execute in family:undersea as @a[tag=family.racing,scores={family.race_cp=9},x=-170,y=42,z=-165,dx=4,dy=4,dz=0] at @s run function family:undersea/race/cp/9
execute in family:undersea as @a[tag=family.racing,scores={family.race_cp=10},x=-171,y=39,z=-156,dx=6,dy=6,dz=0] at @s run function family:undersea/race/cp/10
execute in family:undersea as @a[tag=family.racing,scores={family.race_cp=11},x=-164,y=44,z=-144,dx=4,dy=4,dz=0] at @s run function family:undersea/race/cp/11
execute in family:undersea as @a[tag=family.racing,scores={family.race_cp=12},x=-171,y=39,z=-126,dx=6,dy=6,dz=0] at @s run function family:undersea/race/finish
execute as @a[tag=family.racing] at @s run function family:undersea/race/racer
