import logging

def setup_logger(config):
    """Configures the logging system based on the provided Config object."""
    logger = logging.getLogger("specc") # Named logger is better for debugging
    
    # Prevent duplicate handlers if setup_logger is called multiple times
    if not logger.handlers:
        handler = logging.FileHandler(config.log_file)
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        
    return logger