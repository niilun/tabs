def show_error(title: str, message: str):
    from CTkMessagebox import CTkMessagebox
    CTkMessagebox(title = title, message = message, icon = 'assets/ui/exit.png')

def show_info(title: str, message: str):
    from CTkMessagebox import CTkMessagebox
    CTkMessagebox(title = title, message = message, icon = 'assets/ui/info.png')

def show_ask_question(title: str, question: str) -> bool:
    from CTkMessagebox import CTkMessagebox
    box = CTkMessagebox(title = title, message = question, icon = 'assets/ui/settings.png', option_1 = 'Yes', option_2 = 'No')
    response = box.get()

    if response == 'Yes':
        return True
    return False