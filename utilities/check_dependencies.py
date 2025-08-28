def check_dependencies():
    # if system packages are frozen, we're running inside a bundled exe and can skip dependency checks
    import sys, subprocess, platform
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return
    
    # requirements mapped by pip package name to import name, some are different
    requirements = {
        'pyinstaller': 'PyInstaller',
        'requests': 'requests',
        'configparser': 'configparser',
        'customtkinter': 'customtkinter',
        'ctklistbox': 'CTkListbox',
        'ctkmessagebox': 'CTkMessagebox'
    }
    missing = []
    # try and import packages, if they fail to import add their pip name as missing
    for pip_name, import_name in requirements.items():
        try:
            __import__(import_name)
        except ImportError:
            missing.append(pip_name)

    if missing:
        print(f'Found missing packages: {", ".join(missing)}')
        print('Installing them... Please wait.')
        python_path = sys.executable
        try:
            # check pip availability
            try:
                subprocess.check_call([python_path, '-m', 'pip', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                # use ensurepip to try and install it automatically
                try:
                    subprocess.check_call([python_path, '-m', 'ensurepip'])
                except Exception:
                    # if ensurepip fails, suggest manual install
                    print('Pip is not installed and ensurepip is not available. Please install pip manually.')
                    return
            # Linux distos seem to require the --break-system-packages flag on install
            if platform.system() == 'Linux' or 'Darwin':
                subprocess.check_call([python_path, '-m', 'pip', 'install', *missing, '--break-system-packages'], stdout=subprocess.DEVNULL)
                print('Installing tk... you may need to input your user password for sudo.')
                subprocess.check_call(['sudo' 'apt-get' 'install' 'python3-tk'])
            else:
                subprocess.check_call([python_path, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)
        except Exception:
            print('Failed to install dependencies. Try running "pip install -r requirements.txt" from your terminal while in the TABS root folder.')