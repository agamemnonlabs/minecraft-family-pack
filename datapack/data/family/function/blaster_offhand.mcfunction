advancement revoke @s only family:blaster_offhand
item replace entity @s weapon.offhand with air
give @s minecraft:crossbow[item_model="family:foam_blaster",custom_name={"text": "Foam Blaster", "color": "gold", "italic": false},lore=[{"text": "Foam darts only. Pew pew!", "color": "gray", "italic": false}],use_cooldown={"seconds": 0.4, "cooldown_group": "pewpew:gun_foam_blaster"},custom_data={"PublicBukkitValues": {"pewpew:item_id": "foam_blaster"}},charged_projectiles=[{"id": "minecraft:arrow"}]]
