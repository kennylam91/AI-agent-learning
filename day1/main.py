import dotenv
import random


def append_element(my_list: list = []):
    my_list.append(random.random())
    return my_list


def check_truthiness(value) -> bool:
    if value:
        return True
    else:
        return False


def main():
    print("main func executed")
    print(dotenv.dotenv_values())

    # is None
    result = None
    if result is None:
        print("No result yet")  # should print this line
    else:
        print("Result is ready")

    # mutable defaults
    print(append_element())
    print(append_element())  # the default arg my_list has 2 elements

    # truthiness
    print(check_truthiness(None))  # expected: False
    print(check_truthiness([]))  # expected: False
    print(check_truthiness({}))  # expected: False
    print(check_truthiness(False))  # expected: False
    print(check_truthiness(""))  # expected: False
    print(check_truthiness("hello"))  # expected: True

    # unpacking
    numbers = (1, 2, 3, 4, 5)
    first, second, *rest = numbers
    print(rest)  # expected: 3,4,5

    my_name: str = "lam"
    print(type(my_name))


if __name__ == "__main__":
    main()
