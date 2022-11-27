import enum
import solver
import matplotlib.pyplot as plt
import numpy as np
import tree
from typing import List

np.random.seed(1001)
MAX_NEST_LEVEL = 20


class Rules(enum.Enum):
  NULL = 0  # S --> NULL
  WRAP = 1  # S --> OPEN_CHAR S CLOSED_CHAR
  DOUBLE = 2  # S --> S S


def rewrite_variable(nest_level: int = 0, max_nest_level: int = MAX_NEST_LEVEL):

  if nest_level == 0:
    rewrite_rule = np.random.choice([1, 2])
  else:
    rewrite_rule = np.random.choice(3)

  if nest_level > MAX_NEST_LEVEL:
    rewrite_rule = Rules.NULL.value

  if rewrite_rule == Rules.NULL.value:
    return None

  if rewrite_rule == Rules.WRAP.value:
    open_char, closed_char = np.random.choice(
      ['{}', '()', '<>', '[]'], 
    )
    return [open_char, rewrite_variable(nest_level + 1, max_nest_level), closed_char]

  if rewrite_rule == Rules.DOUBLE.value:
    return [rewrite_variable(nest_level + 1, max_nest_level), rewrite_variable(nest_level + 1, max_nest_level)]
    

def generate_line(min_len: int = 90,
                  max_len: int = 120,
                  max_nest_level: int = MAX_NEST_LEVEL) -> str:
  flattened = tree.flatten(rewrite_variable(0, max_nest_level))
  flattened = [f for f in flattened if f]
  final_string = ''.join(flattened)
  if len(final_string) > max_len or len(final_string) < min_len:
    return generate_line(min_len, max_len, max_nest_level)
  return final_string

def corrupt(symbol):
  all_symbols = list('[{(<>)}]')
  new_symbol = np.random.choice(all_symbols)
  if new_symbol == symbol:
    return corrupt(symbol)
  return new_symbol


def corrupt_line(line):
  corrupt_position = np.random.randint(len(line)) 

  new_symbol = corrupt(line[corrupt_position])
  corrupted_line = list(line)
  corrupted_line[corrupt_position] = new_symbol
  return "".join(corrupted_line), corrupt_position

def generate_lines(num_lines: int,
                   min_len: int = 90,
                   max_len: int = 120,
                   max_nest_level: int = MAX_NEST_LEVEL
                   ):
  lines = []
  for i in range(num_lines):
    if i % 1000 == 0:
      print(f'Working on example: {i}')
    lines.append(generate_line(min_len, max_len, max_nest_level))
  return lines


def plot_length_histograms(max_nest_levels: List[int]):
  lens_by_nest_level = {
    nest_level: [len(x) for x in generate_lines(1000, 10, 120, nest_level)]
        for nest_level in max_nest_levels
  }
  fig, axs = plt.subplots(len(max_nest_levels))
  for idx, nest_level in enumerate(lens_by_nest_level.keys()):
    axs[idx].hist(lens_by_nest_level[nest_level])
  plt.show()
  
# plot_length_histograms([30, 40])

if __name__ == '__main__':
  lines = generate_lines(5_000_000, 10, 120, 40)

if False:
  lengths = []
  max_length = 0
  for i in range(100):
    flattened = tree.flatten(rewrite_variable())
    flattened = [f for f in flattened if f]
    final_string = ''.join(flattened)
    max_length = max(max_length, len(final_string))
    lengths.append(len(final_string))
    if i > 90 and len(final_string) > 0:
      final_string, corrupt_position = corrupt_line(final_string)
    print(final_string)
    found_errors = solver.check_line(final_string, False) 
    if found_errors:
      print('Found error')
  print(lengths)
  print(f'Maximum length generated: {max_length}.')

