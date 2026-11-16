tag @s remove family.swing
execute if score @s family.kswcd matches 1.. run return 0
execute if items entity @s weapon.mainhand minecraft:diamond_sword[minecraft:custom_data~{family_katana:"flame"}] run return run function family:katana/flame/swing
execute if items entity @s weapon.mainhand minecraft:diamond_sword[minecraft:custom_data~{family_katana:"water"}] run return run function family:katana/water/swing
execute if items entity @s weapon.mainhand minecraft:diamond_sword[minecraft:custom_data~{family_katana:"thunder"}] run return run function family:katana/thunder/swing
execute if items entity @s weapon.mainhand minecraft:diamond_sword[minecraft:custom_data~{family_katana:"wind"}] run return run function family:katana/wind/swing
