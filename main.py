import argparse
import logging
import sys

from fabula_helper.config.config import load_settings
from fabula_helper.importers.import_context_factory import ImportContextFactory
from fabula_helper.importers.import_pipeline import ImportPipeline
from fabula_helper.importers.import_targets import ImportTarget


logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Importador de dados do Fabula Ultima Helper."
    )

    parser.add_argument(
        "--only",
        choices=ImportPipeline.available_targets(),
        default=ImportTarget.ALL.value,
        help="Define qual grupo de dados será importado.",
    )

    parser.add_argument(
        "--list-targets",
        action="store_true",
        help="Lista os grupos de importação disponíveis e encerra.",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Ativa logs detalhados.",
    )

    return parser.parse_args()


def configure_logging(debug: bool = False) -> None:
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
        stream=sys.stdout,
    )


def main() -> None:
    args = parse_args()
    configure_logging(debug=args.debug)

    settings = load_settings()

    context = ImportContextFactory.create(settings)
    pipeline = ImportPipeline(context)

    if args.list_targets:
        print(pipeline.list_targets())
        return

    logger.info("Iniciando importação - only=%s", args.only)

    pipeline.run(only=args.only)


if __name__ == "__main__":
    main()