from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
JSON_DIR = PROJECT_ROOT / "jsons"

@dataclass(frozen=True)
class ImportDefinition:
    path: str
    json_file: Path
    identifier: str


SESSION = ImportDefinition(
    path="admin/sessions",
    json_file= JSON_DIR / "sessions_request.json",
    identifier="title",
)

LOCATION = ImportDefinition(
    path="admin/locations",
    json_file= JSON_DIR / "locations_request.json",
    identifier="name",
)

FACTION = ImportDefinition(
    path="admin/factions",
    json_file= JSON_DIR / "factions_request.json",
    identifier="name",
)

WEAPON = ImportDefinition(
    path="admin/items",
    json_file= JSON_DIR / "weapons_request.json",
    identifier="name",
)

ARMOR = ImportDefinition(
    path="admin/items",
    json_file= JSON_DIR / "armor_request.json",
    identifier="name",
)

SHIELD = ImportDefinition(
    path="admin/items",
    json_file= JSON_DIR / "shield_request.json",
    identifier="name",
)

ACCESSORY = ImportDefinition(
    path="admin/items",
    json_file= JSON_DIR / "accessory_request.json",
    identifier="name",
)

ARTIFACT = ImportDefinition(
    path="admin/items",
    json_file= JSON_DIR / "artifact_request.json",
    identifier="name",
)

JOB = ImportDefinition(
    path="admin/jobs",
    json_file= JSON_DIR / "job_request.json",
    identifier="name",
)

JOB_QUESTION = ImportDefinition(
    path="admin/jobs/questions",
    json_file= JSON_DIR / "job_question_request.json",
    identifier="question",
)

JOB_ALIAS = ImportDefinition(
    path="admin/jobs/aliases",
    json_file= JSON_DIR / "job_alias_request.json",
    identifier="alias",
)

JOB_POWER = ImportDefinition(
    path="admin/powers",
    json_file= JSON_DIR / "job_power_request.json",
    identifier="name",
)

JOB_SPELL = ImportDefinition(
    path="admin/spells",
    json_file= JSON_DIR / "job_spell_request.json",
    identifier="name",
)

MONSTER = ImportDefinition(
    path="admin/monsters",
    json_file= JSON_DIR / "monster_request.json",
    identifier="name",
)

MONSTER_TRAIT = ImportDefinition(
    path="admin/monsters/traits",
    json_file= JSON_DIR / "monster_traits_request.json",
    identifier="trait",
)

MONSTER_AFFINITY = ImportDefinition(
    path="admin/monsters/affinities",
    json_file= JSON_DIR / "monster_affinities_request.json",
    identifier="monster_id",
)

MONSTER_ACTION = ImportDefinition(
    path="admin/monsters/actions",
    json_file= JSON_DIR / "monster_actions_request.json",
    identifier="name",
)

NPC = ImportDefinition(
    path="admin/npcs",
    json_file= JSON_DIR / "npc_request.json",
    identifier="name",
)

SPECIAL_RULES = ImportDefinition(
    path="admin/npcs/special",
    json_file= JSON_DIR / "npc_rules_request.json",
    identifier="title",
)

NPC_INVENTORY = ImportDefinition(
    path="admin/npcs/inventory",
    json_file= JSON_DIR / "npc_inventory_request.json",
    identifier="npc_id",
)

NPC_EQUIPMENT = ImportDefinition(
    path="admin/npcs/equipment",
    json_file= JSON_DIR / "npc_equipment_request.json",
    identifier="npc_id",
)

ARCANA = ImportDefinition(
    path="admin/arcanas",
    json_file= JSON_DIR / "arcana_request.json",
    identifier="name",
)

PLAYER = ImportDefinition(
    path="admin/pcs",
    json_file= JSON_DIR / "player_request.json",
    identifier="name",
)

PLAYER_EQUIPMENT = ImportDefinition(
    path="admin/pcs/equipments",
    json_file= JSON_DIR / "player_equipment_request.json",
    identifier="pc_id",
)

PLAYER_INVENTORY = ImportDefinition(
    path="admin/pcs/inventories",
    json_file= JSON_DIR / "player_inventory_request.json",
    identifier="pc_id",
)

PLAYER_JOB = ImportDefinition(
    path="admin/pcs/jobs",
    json_file= JSON_DIR / "player_job_request.json",
    identifier="job_id",
)

PLAYER_POWER = ImportDefinition(
    path="admin/pcs/powers",
    json_file= JSON_DIR / "player_power_request.json",
    identifier="power_id",
)

PLAYER_SPELL = ImportDefinition(
    path="admin/pcs/spells",
    json_file= JSON_DIR / "player_spells_request.json",
    identifier="spell_id",
)

PLAYER_MONSTER_SPELL = ImportDefinition(
    path="admin/pcs/monster-spells",
    json_file= JSON_DIR / "player_monster_spell_request.json",
    identifier="monster_action_id",
)

PLAYER_ARCANA = ImportDefinition(
    path="admin/pcs/arcanas",
    json_file= JSON_DIR / "player_arcana_request.json",
    identifier="arcana_id",
)

PLAYER_BOND = ImportDefinition(
    path="admin/pcs/bonds",
    json_file= JSON_DIR / "player_bond_request.json",
    identifier="target_name",
)

