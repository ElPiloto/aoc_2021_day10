import enum
import solver
import numpy as np
import tree

np.random.seed(1001)
MAX_NEST_LEVEL = 15


class Rules(enum.Enum):
  NULL = 0  # S --> NULL
  WRAP = 1  # S --> OPEN_CHAR S CLOSED_CHAR
  DOUBLE = 2  # S --> S S


def rewrite_variable(nest_level: int = 0):

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
    return [open_char, rewrite_variable(nest_level + 1), closed_char]

  if rewrite_rule == Rules.DOUBLE.value:
    return [rewrite_variable(nest_level + 1), rewrite_variable(nest_level + 1)]
    

def generate_input(max_len: int = 120) -> str:
  flattened = tree.flatten(rewrite_variable())
  flattened = [f for f in flattened if f]
  final_string = ''.join(flattened)
  if len(final_string) > max_len:
    return generate_input(max_len)
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
  return "".join(corrupted_line)


max_length = 0
for i in range(100):
  flattened = tree.flatten(rewrite_variable())
  flattened = [f for f in flattened if f]
  final_string = ''.join(flattened)
  max_length = max(max_length, len(final_string))
  if i > 90 and len(final_string) > 0:
    final_string = corrupt_line(final_string)
  print(final_string)
  found_errors = solver.check_line(final_string, False) 
  if found_errors:
    print('Found error')
print(f'Maximum length generated: {max_length}.')
