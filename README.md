# Family Minecraft server pack

Original art and sounds for our family Paper server (Minecraft 26.3, Java + Bedrock via Geyser):

- **Foam Blaster**: the Pewpew `foam_blaster` gun (item model `family:foam_blaster`).
  Crafted from crossbow + amethyst shard + orange dye.
  Main hand only: one put in the off-hand goes back to the inventory.
- **Lightsabers**: 7 colours, separate items on top of a diamond sword (item model `family:lightsaber_<colour>`).
  Crafted from diamond sword + amethyst shard + dye; hitting something plays a "vwoom".

| File | Goes to |
|---|---|
| `dist/family-pack-java.zip` | `server.properties` `resource-pack` (PC players) |
| `dist/family-pack-bedrock.mcpack` | `plugins/Geyser-Spigot/packs/` (iPads) |
| `geyser/custom_mappings/family.json` | `plugins/Geyser-Spigot/custom_mappings/` |
| `dist/family-datapack.zip` | `world/datapacks/` (recipes, hit sound, blaster main-hand lock) |

Rebuild after editing `art.py` / `sounds.py`: `python3 build.py` (needs Pillow and `oggenc` from vorbis-tools).
The server links to a specific commit, so a rebuild only goes live once that link and its sha1 are updated.
