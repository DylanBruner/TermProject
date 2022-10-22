def generateHelpMenu(menu: dict) -> str:
    helpMenu = ""

    for header, options in menu.items():
        #Make the descriptions all start at the same place
        maxLen = 0
        for option, description in options.items():
            if len(option) > maxLen:
                maxLen = len(option)
        helpMenu += f"{header}\n"
        for option, description in options.items():
            helpMenu += f"    {option}{' '*(maxLen-len(option))} - {description}\n"

        helpMenu += "\n"

    return helpMenu
