execute as @a[scores={family.kcd=1}] run title @s actionbar {"text": "Special move ready!", "color": "gray"}
scoreboard players remove @a[scores={family.kcd=1..}] family.kcd 1
scoreboard players remove @a[scores={family.kswcd=1..}] family.kswcd 1
execute as @a[tag=family.swing] at @s run function family:katana/swing
execute as @a[scores={family.kfr=1..}] at @s run function family:katana/frame
