from typing import Any

from fabula_helper.utils.json_loader import load_json_array
from fabula_helper.definitions.request_definitions import ImportDefinition


class FactionNormalizer:
    def replace_location_names_by_ids(
        self,
        normalized_locations: dict[str, Any],
        definition: ImportDefinition,
    ) -> list[dict[str, Any]]:
        factions = load_json_array(definition.json_file)

        for faction_index, faction in enumerate(factions):
            raw_relations = (
                faction.get("faction_location_relation")
                or faction.get("location")
                or []
            )

            if not isinstance(raw_relations, list):
                raise RuntimeError(
                    "faction_location_relation inválido, esperado array.\n"
                    f"Índice da faction no JSON: {faction_index}\n"
                    f"Faction: {faction}"
                )

            normalized_relations = []

            for relation_index, relation in enumerate(raw_relations):
                location_name = relation.get("name")
                relation_type = relation.get("relation_type")

                if not isinstance(location_name, str):
                    raise RuntimeError(
                        "location.name inválido na relação da faction.\n"
                        f"Índice da faction no JSON: {faction_index}\n"
                        f"Índice da relation no JSON: {relation_index}\n"
                        f"Valor recebido: {location_name!r}\n"
                        f"Faction: {faction}"
                    )

                if not isinstance(relation_type, str):
                    raise RuntimeError(
                        "relation_type inválido na relação da faction.\n"
                        f"Índice da faction no JSON: {faction_index}\n"
                        f"Índice da relation no JSON: {relation_index}\n"
                        f"Valor recebido: {relation_type!r}\n"
                        f"Faction: {faction}"
                    )

                location_id = normalized_locations.get(location_name)

                if location_id is None:
                    raise RuntimeError(
                        "Location não encontrada no mapa de locations.\n"
                        f"Valor procurado: {location_name}\n"
                        f"Índice da faction no JSON: {faction_index}\n"
                        f"Índice da relation no JSON: {relation_index}\n"
                        f"Faction: {faction}"
                    )

                normalized_relations.append(
                    {
                        "location_id": location_id,
                        "relation_type": relation_type,
                    }
                )

            faction["faction_location_relation"] = normalized_relations

            if "location" in faction:
                del faction["location"]

        return factions