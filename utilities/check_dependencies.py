def check_dependencies():
    import pkg_resources, sys, subprocess, platform

    requirements = {'pyinstaller', 'requests', 'configparser', 'customtkinter', 'ctklistbox', 'ctkmessagebox'}
    found = {pkg.key for pkg in pkg_resources.working_set}
    missing = requirements - found

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