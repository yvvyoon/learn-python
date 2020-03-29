def print_menu():
    print('1. 전화번호 출력')
    print('2. 전화번호 추가')
    print('3. 전화번호 삭제')
    print('4. 전화번호 찾기')
    print('5. 종료')


def print_dic(numbers):
    print('전화번호: ')

    for name in numbers:
        print(f'이름: {name}, 번호: {numbers[name]}')


def add_member():
    print('이름과 번호 추가')

    name = input('이름: ')
    phone = input('번호: ')
    numbers[name] = phone


def delete_member(numbers):
    print('이름과 번호 삭제')

    name = input('이름: ')

    if name in numbers:
        print(f'번호: {numbers[name]}')
    else:
        print(f'{name}을 찾을 수 없습니다.')


def lookup_member(numbers):
    print('번호 찾기')

    name = input('이름: ')

    if name in numbers:
        print(f'번호: {numbers[name]}')
    else:
        print(f'{name}을 찾을 수 없습니다.')


numbers = {}
menu_choice = 0
print_menu()

while menu_choice != 5:
    menu_choice = int(input('번호를 입력하세요: '))

    if menu_choice == 1:
        print_dic(numbers)
    elif menu_choice == 2:
        add_member()
    elif menu_choice == 3:
        delete_member(numbers)
    elif menu_choice == 4:
        lookup_member(numbers)
    elif menu_choice == 5:
        print_menu()
