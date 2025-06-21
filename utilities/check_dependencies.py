def check_dependencies():
    import pkg_resources, sys, subprocess

    requirements = {'pyinstaller', 'requests', 'configparser', 'customtkinter', 'ctklistbox', 'ctkmessagebox'}
    found = {pkg.key for pkg in pkg_resources.working_set}
    missing = requirements - found

    if missing:
        print(f'Found missing packages: {", ".join(missing)}')
        print('Installing them... Please wait.')
        python_path = sys.executable
        try:
            subprocess.check_call([python_path, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)
        except Exception:
            print('Failed to install dependencies. Try running "pip install -r requirements.txt" from your terminal while in the TABS root folder.')