from random import random, shuffle
import fileinput


def random_items(iterable, k=1):
	result = [None] * k
	for i, item in enumerate(iterable):
		if i < k:
			result[i] = item
		else:
			j = int(random() * (i + 1))
			if j < k:
				result[j] = item
	shuffle(result)
	return result

def lines(filenname):
	for l in fileinput.input(filenname):
		yield l.strip()

def sample_lines_from_file(filenname, k=1):
	return random_items((line.strip() for line in fileinput.input(filenname)), k)
