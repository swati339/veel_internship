import logging
# import colorlogs

def setup_logging(level='INFO'):
    """Set up basic colored logging."""
    logger = logging.getLogger()
    # colorlogs.install(level=level, logger=logger, fmt='%(asctime)s [%(levelname)s] %(name)s: %(message)s')