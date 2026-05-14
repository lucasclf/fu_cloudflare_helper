from dataclasses import dataclass

from fabula_helper.definitions.request_definitions import (
    ACCESSORY,
    ARCANA,
    ARMOR,
    ARTIFACT,
    FACTION,
    JOB,
    JOB_ALIAS,
    JOB_POWER,
    JOB_QUESTION,
    JOB_SPELL,
    LOCATION,
    MONSTER,
    MONSTER_ACTION,
    MONSTER_AFFINITY,
    MONSTER_TRAIT,
    NPC,
    NPC_EQUIPMENT,
    NPC_INVENTORY,
    SPECIAL_RULES,
    PLAYER,
    PLAYER_ARCANA,
    PLAYER_BOND,
    PLAYER_EQUIPMENT,
    PLAYER_INVENTORY,
    PLAYER_JOB,
    PLAYER_MONSTER_SPELL,
    PLAYER_POWER,
    PLAYER_SPELL,
    SESSION,
    SHIELD,
    WEAPON,
)
from fabula_helper.definitions.request_definitions import ImportDefinition


@dataclass(frozen=True)
class SessionImportGroup:
    session: ImportDefinition


@dataclass(frozen=True)
class ArcanaImportGroup:
    arcana: ImportDefinition


@dataclass(frozen=True)
class FactionImportGroup:
    location: ImportDefinition
    faction: ImportDefinition


@dataclass(frozen=True)
class ItemImportGroup:
    weapon: ImportDefinition
    armor: ImportDefinition
    shield: ImportDefinition
    accessory: ImportDefinition
    artifact: ImportDefinition


@dataclass(frozen=True)
class JobImportGroup:
    job: ImportDefinition
    question: ImportDefinition
    alias: ImportDefinition
    power: ImportDefinition
    spell: ImportDefinition


@dataclass(frozen=True)
class MonsterImportGroup:
    monster: ImportDefinition
    trait: ImportDefinition
    affinity: ImportDefinition
    action: ImportDefinition


@dataclass(frozen=True)
class NpcImportGroup:
    npc: ImportDefinition
    special_rule: ImportDefinition
    inventory: ImportDefinition
    equipment: ImportDefinition


@dataclass(frozen=True)
class PcImportGroup:
    player: ImportDefinition
    equipment: ImportDefinition
    inventory: ImportDefinition
    job: ImportDefinition
    power: ImportDefinition
    bond: ImportDefinition
    spell: ImportDefinition
    arcana: ImportDefinition
    monster_spell: ImportDefinition


SESSION_GROUP = SessionImportGroup(
    session=SESSION,
)

ARCANA_GROUP = ArcanaImportGroup(
    arcana=ARCANA,
)

FACTION_GROUP = FactionImportGroup(
    location=LOCATION,
    faction=FACTION,
)

ITEM_GROUP = ItemImportGroup(
    weapon=WEAPON,
    armor=ARMOR,
    shield=SHIELD,
    accessory=ACCESSORY,
    artifact=ARTIFACT,
)

JOB_GROUP = JobImportGroup(
    job=JOB,
    question=JOB_QUESTION,
    alias=JOB_ALIAS,
    power=JOB_POWER,
    spell=JOB_SPELL,
)

MONSTER_GROUP = MonsterImportGroup(
    monster=MONSTER,
    trait=MONSTER_TRAIT,
    affinity=MONSTER_AFFINITY,
    action=MONSTER_ACTION,
)

NPC_GROUP = NpcImportGroup(
    npc=NPC,
    special_rule=SPECIAL_RULES,
    inventory=NPC_INVENTORY,
    equipment=NPC_EQUIPMENT,
)

PC_GROUP = PcImportGroup(
    player=PLAYER,
    equipment=PLAYER_EQUIPMENT,
    inventory=PLAYER_INVENTORY,
    job=PLAYER_JOB,
    power=PLAYER_POWER,
    bond=PLAYER_BOND,
    spell=PLAYER_SPELL,
    arcana=PLAYER_ARCANA,
    monster_spell=PLAYER_MONSTER_SPELL,
)