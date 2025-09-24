"""калькулятор"""
def add(n1, n2):
    """прибавить числа"""
    return n1 + n2

def sub(n1, n2):
    """вычесть числа"""
    return n1 - n2

def mul(n1, n2):
    """умножить"""
    return n1 * n2

def div(n1, n2):
    """разделить числа"""
    if n2 == 0:
        return "Неправильный ввод"
    return n1 / n2

def power(n1, n2):
    """возвести в степень число"""
    return n1 ** n2

def sqrt(n1, n2):
    """взять корень из числа"""
    return n1 ** (1/n2)

def main():
    """основная функция калькулятора"""
  
    sel = int(input("Выберите опцию:\n"
        "1. сумма\n"
        "2. вычитание\n"
        "3. умножение\n"
        "4. разделение\n"
        "5. возведение в степень\n"
        "6. взять корень из числа\n"))

    n1 = int(input("введите первое число: "))
    n2 = int(input("введите второе число( в случае выбора опции 5 и 6 введите степень): "))

    if sel == 1:
        print(add(n1, n2))
    elif sel == 2:
        print(sub(n1, n2))
    elif sel == 3:
        print(mul(n1, n2))
    elif sel == 4:
        print(div(n1, n2))
    elif sel == 5:
        print(power(n1, n2))
    elif sel == 6:
        print(sqrt(n1, n2))
    else:
        print("неправильный ввод")

if __name__ == '__main__':
    main()
