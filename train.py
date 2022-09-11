import re
import argparse
import pickle
from pathlib import Path
from model import Model


def preprocess(text):
    text = text.lower()
    text = re.sub('[^а-яё ]', '', text)
    return list(filter(lambda x: len(x) > 0, text.split()))


def save_model(path, fit_model):
    with open(path) as f:
        pickle.dump(fit_model, f)
        print(f'Модель сохранена в файл {path}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Команды для обучения модели')
    parser.add_argument('--input-dir', type=str, help='Директория, где находятся тексты для обучения модели')
    parser.add_argument('--model', type=str, help='Путь к файлу, где будет сохранена обученная модель')

    arguments = parser.parse_args()
    prefix_size = 2

    if arguments.input_dir is None:
        words = preprocess(input('Введите текст для обучения модели: '))
    else:
        path = Path(arguments.input_dir)
        words = []

        for file in path.iterdir():
            try:
                with open(file) as f:
                    words.extend(preprocess(f.read()))
            except Exception:
                print(f'Не удалось прочитать файл {file}')

    model = Model()

    model.fit(words, prefix_size)

    try:
        save_model(arguments.model, model)
    except Exception:
        print('Не удалось сохранить модель в указанный файл')
