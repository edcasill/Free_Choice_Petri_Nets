import os
import numpy as np


def read_file(file):
    """_summary_

    Args:
        file (_type_): _description_
    """
    with open(file, 'r') as f:
        lines = f.readlines()


def main():
    option = int(input('Selecciona el numero de archivo a analizar: '))
    print(option)

if __name__ == "__main__":
    main()