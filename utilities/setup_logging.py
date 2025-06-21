def setup_logging(log_level: int):
    import logging, sys, os, uuid, datetime

    # Create the 'logs' folder if it doesn't exist
    if not os.path.isdir('logs'):
        os.mkdir('logs')

    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Set formatting (remove time from stdout to not clog console)
    stdout_format = logging.Formatter('%(levelname)s | %(message)s')
    file_format = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

    stdout_logger = logging.StreamHandler(sys.stdout)
    stdout_logger.setFormatter(stdout_format)

    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    current_uuid = uuid.uuid4()

    # Refresh uuid if it somehow already exists
    if os.path.exists(f'logs/{current_time} {current_uuid}.log'):
        current_uuid = uuid.uuid4()
    
    file_logger = logging.FileHandler(f'logs/{current_time} {current_uuid}.log')
    file_logger.setFormatter(file_format)

    logger.addHandler(stdout_logger)
    logger.addHandler(file_logger)