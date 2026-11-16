advancement revoke @s only family:katana_hit_water
execute if entity @s[tag=family.caster] run return 0
function family:katana/water/swing
execute rotated ~ 0 anchored eyes positioned ^ ^-0.4 ^2 run function family:katana/water/burst
