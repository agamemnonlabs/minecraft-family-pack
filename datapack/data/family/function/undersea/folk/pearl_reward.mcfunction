execute unless score @s family.pearls matches 10.. run return fail
execute if entity @s[tag=family.pearls_done] run return fail
tag @s add family.pearls_done
give @s minecraft:gold_nugget[item_name={"text": "Sand Dollar", "color": "yellow"},lore=[{"text": "Spend it at the Bubble Cafe", "color": "gray", "italic": false}],custom_data={"family_coin": 1}] 10
give @s minecraft:tropical_fish_bucket[tropical_fish/pattern="kob",tropical_fish/base_color="orange",tropical_fish/pattern_color="white"]
tellraw @s [{"text": "Mayor Marina", "color": "light_purple"}, {"text": ": Here are 10 Sand Dollars, and a pet fish! Let it out somewhere nice.", "color": "white"}]
execute at @s run playsound minecraft:entity.player.levelup master @s ~ ~ ~
