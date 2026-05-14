import json
import logging
from datetime import datetime
from pathlib import Path

from fabula_helper.importers.import_context import ImportContext
from fabula_helper.importers.import_report import ImportBatchReport, ImportRunReport, ImportStepReport, now_iso
from fabula_helper.importers.import_step import ImportStep
from fabula_helper.importers.import_targets import ImportTarget, import_target_choices
from fabula_helper.definitions.request_groups import (
    ARCANA_GROUP,
    FACTION_GROUP,
    ITEM_GROUP,
    JOB_GROUP,
    MONSTER_GROUP,
    NPC_GROUP,
    PC_GROUP,
    SESSION_GROUP,
)


logger = logging.getLogger(__name__)


class ImportPipeline:
    def __init__(self, context: ImportContext) -> None:
        self._context = context

        self._steps: tuple[ImportStep, ...] = (
            ImportStep(
                target=ImportTarget.SESSIONS,
                label="sessions",
                description="Importa sessões.",
                handler=self._import_sessions,
            ),
            ImportStep(
                target=ImportTarget.ARCANAS,
                label="arcanas",
                description="Importa arcanas.",
                handler=self._import_arcanas,
            ),
            ImportStep(
                target=ImportTarget.LOCATIONS,
                label="locations",
                description="Importa localidades.",
                handler=self._import_locations,
            ),
            ImportStep(
                target=ImportTarget.FACTIONS,
                label="factions",
                description="Importa facções e suas relações com localidades.",
                handler=self._import_factions,
            ),
            ImportStep(
                target=ImportTarget.ITEMS,
                label="items",
                description="Importa armas, armaduras, escudos, acessórios e artefatos.",
                handler=self._import_items,
            ),
            ImportStep(
                target=ImportTarget.JOBS,
                label="jobs",
                description="Importa classes, perguntas, aliases, poderes e magias.",
                handler=self._import_jobs,
            ),
            ImportStep(
                target=ImportTarget.MONSTERS,
                label="monsters",
                description="Importa monstros, traits, afinidades e ações.",
                handler=self._import_monsters,
            ),
            ImportStep(
                target=ImportTarget.NPCS,
                label="npcs",
                description="Importa NPCs, regras especiais, inventário e equipamento.",
                handler=self._import_npcs,
            ),
            ImportStep(
                target=ImportTarget.PCS,
                label="pcs",
                description=(
                    "Importa personagens, inventário, equipamento, classes, poderes, "
                    "magias, magias de monstro, arcanas e vínculos."
                ),
                handler=self._import_pcs,
            ),
        )

        self._steps_by_target: dict[ImportTarget, ImportStep] = {
            step.target: step
            for step in self._steps
        }

    @staticmethod
    def available_targets() -> tuple[str, ...]:
        return import_target_choices()

    def list_targets(self) -> str:
        lines = [
            "Targets disponíveis:",
            "",
            f"{ImportTarget.ALL.value}",
            "  Executa todas as etapas de importação.",
            "",
        ]

        for step in self._steps:
            lines.append(step.target.value)
            lines.append(f"  {step.description}")
            lines.append("")

        return "\n".join(lines)

    def run(self, only: str = ImportTarget.ALL.value) -> None:
        try:
            target = ImportTarget(only)
        except ValueError as error:
            valid_tasks = ", ".join(self.available_targets())
            raise RuntimeError(
                f"Grupo de importação inválido: {only}. Valores aceitos: {valid_tasks}"
            ) from error

        started_at = now_iso()
        step_reports: list[ImportStepReport] = []

        if target == ImportTarget.ALL:
            for step in self._steps:
                step_reports.append(self._run_step(step))
        else:
            step = self._steps_by_target.get(target)

            if step is None:
                valid_tasks = ", ".join(self.available_targets())
                raise RuntimeError(
                    f"Grupo de importação inválido: {target.value}. Valores aceitos: {valid_tasks}"
                )

            step_reports.append(self._run_step(step))

        report = ImportRunReport(
            started_at=started_at,
            finished_at=now_iso(),
            only=target.value,
            steps=step_reports,
        )

        report_path = self._save_report(report)

        logger.info(
            "Processo finalizado | criados=%s | já existiam=%s | erros=%s",
            report.created,
            report.already_exists,
            report.error_count,
        )

        logger.info("Relatório salvo em: %s", report_path)

    @staticmethod
    def _run_step(step: ImportStep) -> ImportStepReport:
        logger.info("Iniciando importação de %s...", step.label)

        batches = step.handler()

        step_report = ImportStepReport(
            target=step.target.value,
            label=step.label,
            batches=batches,
        )

        logger.info(
            "Etapa finalizada: %s | criados=%s | já existiam=%s | erros=%s",
            step.label,
            step_report.created,
            step_report.already_exists,
            step_report.error_count,
        )

        return step_report

    @staticmethod
    def _save_report(report: ImportRunReport) -> Path:
        reports_dir = Path("../../reports")
        reports_dir.mkdir(exist_ok=True)

        filename = datetime.now().strftime("import-report-%Y%m%d-%H%M%S.json")
        report_path = reports_dir / filename

        report_path.write_text(
            json.dumps(
                report.to_dict(),
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return report_path

    def _import_sessions(self) -> list[ImportBatchReport]:
        return [
            self._context.batch_import_service.import_from_definition(
                SESSION_GROUP.session,
                label="sessions",
            )
        ]

    def _import_arcanas(self) -> list[ImportBatchReport]:
        return [
            self._context.batch_import_service.import_from_definition(
                ARCANA_GROUP.arcana,
                label="arcanas",
            )
        ]

    def _import_locations(self) -> list[ImportBatchReport]:
        return [
            self._context.batch_import_service.import_from_definition(
                FACTION_GROUP.location,
                label="locations",
            )
        ]

    def _import_factions(self) -> list[ImportBatchReport]:
        return self._context.faction_import_service.create_entities(
            faction_definition=FACTION_GROUP.faction,
        )

    def _import_items(self) -> list[ImportBatchReport]:
        reports: list[ImportBatchReport] = []

        reports.append(
            self._context.batch_import_service.import_from_definition(
                ITEM_GROUP.weapon,
                label="weapons",
            )
        )
        reports.append(
            self._context.batch_import_service.import_from_definition(
                ITEM_GROUP.armor,
                label="armors",
            )
        )
        reports.append(
            self._context.batch_import_service.import_from_definition(
                ITEM_GROUP.shield,
                label="shields",
            )
        )
        reports.append(
            self._context.batch_import_service.import_from_definition(
                ITEM_GROUP.accessory,
                label="accessories",
            )
        )
        reports.append(
            self._context.batch_import_service.import_from_definition(
                ITEM_GROUP.artifact,
                label="artifacts",
            )
        )

        return reports

    def _import_jobs(self) -> list[ImportBatchReport]:
        return self._context.job_import_service.create_jobs_with_dependencies(
            job_definition=JOB_GROUP.job,
            question_definition=JOB_GROUP.question,
            alias_definition=JOB_GROUP.alias,
            power_definition=JOB_GROUP.power,
            spell_definition=JOB_GROUP.spell,
        )

    def _import_monsters(self) -> list[ImportBatchReport]:
        return self._context.monster_import_service.create_monsters_with_dependencies(
            monster_definition=MONSTER_GROUP.monster,
            trait_definition=MONSTER_GROUP.trait,
            affinity_definition=MONSTER_GROUP.affinity,
            action_definition=MONSTER_GROUP.action,
        )

    def _import_npcs(self) -> list[ImportBatchReport]:
        return self._context.npc_import_service.create_npcs_with_dependencies(
            npc_definition=NPC_GROUP.npc,
            special_rules_definition=NPC_GROUP.special_rule,
            npc_inventory_definition=NPC_GROUP.inventory,
            npc_equipment_definition=NPC_GROUP.equipment,
        )

    def _import_pcs(self) -> list[ImportBatchReport]:
        return self._context.pc_import_service.create_pcs_with_dependencies(
            pc_definition=PC_GROUP.player,
            equip_definition=PC_GROUP.equipment,
            inventory_definition=PC_GROUP.inventory,
            job_definition=PC_GROUP.job,
            power_definition=PC_GROUP.power,
            bond_definition=PC_GROUP.bond,
            spell_definition=PC_GROUP.spell,
            arcana_definition=PC_GROUP.arcana,
            player_monster_spell_definition=PC_GROUP.monster_spell,
        )