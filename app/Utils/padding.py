lebar = 60

def pad_center(text):
    return text.center(lebar)

def pad_left(text):
    return text.ljust(lebar)

def pad_right(text):
    return text.rjust(lebar)

def pad_both(text):
    padding = (lebar - len(text)) // 2
    return ' ' * padding + text + ' ' * padding

def pad_top(lines=1):
    return '\n' * lines
def pad_bottom(lines=1):
    return '\n' * lines
def pad_all_sides(text, lines=1):
    padding = '\n' * lines
    return f"{padding}{text}{padding}"