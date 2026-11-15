# Family Minecraft server pack

Original art and sounds for our family Paper server (Minecraft 26.3, Java + Bedrock via Geyser):

- **Foam Blaster**: the Pewpew `foam_blaster` gun (item model `family:foam_blaster`).
  Crafted from crossbow + amethyst shard + orange dye.
  Main hand only: one put in the off-hand goes back to the inventory.
- **Lightsabers**: 7 colours, separate items on top of a diamond sword (item model `family:lightsaber_<colour>`).
  Crafted from diamond sword + amethyst shard + dye; hitting something plays a "vwoom".
- **The Undersea** (`undersea.py`, art in `undersea_art.py`): dimension `family:undersea`, vanilla overworld
  terrain with the sea level raised to 100 and only vanilla ocean biomes (Bedrock players can't see custom
  biomes). Everyone there gets conduit power (breathing + underwater sight).
  - Getting there: whirlpool portals, or the **Bubble Shell** (kelp + sand + glass bottle; hold use for 1 s,
    it takes you to the hub and back to where you left).
  - **Shark costume**: hood, suit, pants, flippers. Crafted from the diamond piece + grey dye + white dye.
    Same protection as diamond, unbreakable.
  - Admin, once after the first start: `/function family:undersea/gamerules` (only if gamerules are
    per-dimension on the server), then `/function family:undersea/build_hub`.
  - Admin, where a portal should go: stand there and run `/function family:portal_here` (replaces a 5x5x3
    area under your feet). `/function family:portal_remove` next to one removes its trigger.

| File | Goes to |
|---|---|
| `dist/family-pack-java.zip` | `server.properties` `resource-pack` (PC players) |
| `dist/family-pack-bedrock.mcpack` | `plugins/Geyser-Spigot/packs/` (iPads) |
| `geyser/custom_mappings/family.json` | `plugins/Geyser-Spigot/custom_mappings/` |
| `dist/family-datapack.zip` | `world/datapacks/` (recipes, hit sound, blaster main-hand lock) |

Rebuild after editing `art.py` / `sounds.py`: `python3 build.py` (needs Pillow and `oggenc` from vorbis-tools).
The server links to a specific commit, so a rebuild only goes live once that link and its sha1 are updated.
