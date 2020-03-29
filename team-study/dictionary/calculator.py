def add(a, b):
    return a + b


def sub(a, b):
    return a - b


def mul(a, b):
    return a * b


def div(a, b):
    return a / b


def choose_menu():
    print('What do you want to do?')
    print('add, sub, mul, div, exit')
    
    return input('Your choice: ')


menu = {
    'add': add,
    'sub': sub,
    'mul': mul,
    'div': div,
}
choice = choose_menu()

while choice is not 'exit':
    if choice in menu:
        x = int(input('First value: '))
        y = int(input('Second value: '))

        print(menu[choice](x, y))

    choice = choose_menu()