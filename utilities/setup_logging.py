def setup_logging(log_level: int):
    """
    Creates and configures logging for both console and file output.

    This function sets up a root logger with two handlers:
        - a console logger to stdout
        - file logger, in a uniquely named file comprised of a timestamp and unique UUID

    Inputs:
        - log_level (int) is the log level value to be passed to the root logger.
    
    Outputs:
        - log_path (string) is the relative logs/ path to the log file.
    """
    import logging, sys, os, uuid, datetime

    # create the 'logs' folder if it doesn't exist
    if not os.path.isdir('logs'):
        os.mkdir('logs')

    logger = logging.getLogger()
    logger.setLevel(log_level)

    # set formatting (remove time from stdout to not clog console)
    stdout_format = logging.Formatter('%(levelname)s | %(message)s')
    file_format = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

    stdout_logger = logging.StreamHandler(sys.stdout)
    stdout_logger.setFormatter(stdout_format)

    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    current_uuid = uuid.uuid4()

    # refresh uuid if it somehow already exists
    if os.path.exists(f'logs/{current_time} {current_uuid}.log'):
        current_uuid = uuid.uuid4()
    
    log_path = f'logs/{current_time} {current_uuid}.log'
    file_logger = logging.FileHandler(log_path)
    file_logger.setFormatter(file_format)

    logger.addHandler(stdout_logger)
    logger.addHandler(file_logger)
    return log_path