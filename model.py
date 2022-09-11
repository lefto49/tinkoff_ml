import random
import numpy as np


class Model:
    def __init__(self):
        self.prefix_dict = {}

    def set_seed(self, seed):
        random.seed(seed)

    def fit(self, words, prefix_size):
        for i in range(0, len(words) - prefix_size):
            cur_key = tuple(words[i:i + prefix_size])
            next_word = words[i + prefix_size]

            if cur_key in self.prefix_dict.keys():
                if next_word in self.prefix_dict[cur_key].keys():
                    self.prefix_dict[cur_key][next_word] += 1
                else:
                    self.prefix_dict[cur_key][next_word] = 1
            else:
                self.prefix_dict[cur_key] = {next_word: 1}

        for prefix in self.prefix_dict.keys():
            counter = sum(self.prefix_dict[prefix].values())
            for next_word in self.prefix_dict[prefix].keys():
                self.prefix_dict[prefix][next_word] /= counter

    def generate(self, seq_length, prefix):
        if prefix is None:
            index = random.randint(0, len(self.prefix_dict))
            prefix = list(self.prefix_dict.keys())[index]

        if tuple(prefix) not in self.prefix_dict.keys():
            return ' '.join(prefix)

        prefix_start = 0
        prefix_len = len(prefix)
        while len(prefix) < seq_length:
            cur_prefix = tuple(prefix[prefix_start:prefix_start + prefix_len])
            if cur_prefix not in self.prefix_dict.keys():
                break

            prefix.append(np.random.choice(a=list(self.prefix_dict[cur_prefix].keys()),
                                           p=list(self.prefix_dict[cur_prefix].values())))
            prefix_start += 1

        return ' '.join(prefix)
