def bold(text):
    bold_start = '\033[1m'
    bold_end = '\033[1m'
    return bold_start + text + bold_end

def blue(text):
    blue_start = '\033[34m'
    blue_end = '\033[0m'
    return blue_start + text + blue_end

def red(text):
    red_start = '\033[31m'
    red_end = '\033[0m'
    return red_start + text + red_end