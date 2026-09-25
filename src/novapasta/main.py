import logging

from novapasta.config.logging_config import configurar_logging


def main():
    configurar_logging()

    log = logging.getLogger(__name__)

    log.info("Aplicação iniciada.")


if __name__ == "__main__":
    main()
