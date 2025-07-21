from utilities.clear_console import clear_console

def reload_game():
    '''Reloads the game by re-running python.'''
    import os, sys, logging
    # Flush buffers so they are closed properly
    sys.stdout.flush()
    sys.stderr.flush()
    clear_console()
    logging.info(f'Reloading game, running {" ".join(sys.orig_argv)}')
    os.execl(sys.executable, *sys.orig_argv)