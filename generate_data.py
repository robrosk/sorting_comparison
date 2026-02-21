import random

def generate_random_array(n, seed):
    random.seed(seed)
    return [random.random() for _ in range(n)]

