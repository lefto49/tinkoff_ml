import argparse
import pickle
from model import Model
from train import preprocess


def restore_model(path):
    with open(path) as file:
        loaded_model = pickle.load(file)
    return loaded_model


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Команды для генерации текста')
    parser.add_argument('--model', type=str, help='Путь к файлу, где хранится обученная модель')
    parser.add_argument('--prefix', type=str, help='Начало генерируемой последовательности')
    parser.add_argument('--length', type=int, help='Длина генерируемой последовательности')

    arguments = parser.parse_args()

    if arguments.model is None:
        print('Необходимо указать путь к файлу, где хранится обученная модель')
        exit()

    if arguments.length is None:
        print('Необходимо указать длину генерируемой последовательности')
        exit()

    prefix = None
    if arguments.prefix is not None:
        prefix = preprocess(arguments.prefix)

    try:
        model = restore_model(arguments.model)
        print(model.generate(arguments.length, prefix))
    except Exception:
        print('Не удалось восстановить модель')
