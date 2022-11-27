import generator
import solver

from absl import logging
import numpy as np

DEFAULT_INPUT_FILE = 'one_million_lines.txt'


INPUT_LINE_CHAR_NUM_MAPPING = {
  '{': 0,
  '}': 1,
  '(': 2,
  ')': 3,
  '[': 4,
  ']': 5,
  '<': 6,
  '>': 7
}

def map_input_line_to_numbers(line: str):
  new_line = ''
  for x in line:
    new_line += str(INPUT_LINE_CHAR_NUM_MAPPING[x])
  return new_line


def make_out_file(input_file: str, prefix: str,
                  version_number: str, corrupt_percentage: float):
  return input_file.replace('.txt', 
                            f'_v{version_number}_{prefix}_corrupt_'
                            f'{corrupt_percentage*100.}_percent.txt')


def finalize_dataset(corrupt_percentage: float,
                     version_number: str,
                     input_file: str =  DEFAULT_INPUT_FILE):
  """Returns corrupted and uncorrupted lines."""
  f = open(input_file, "r")
  lines = f.readlines()

  input_lines = []
  output_lines = []
  logging.set_verbosity(logging.INFO)
  for idx, line in enumerate( lines ):
    line = line.replace('\n', '')
    if idx % 1000 == 0:
      logging.info('Working on example %d', idx)
    if np.random.rand() >= corrupt_percentage:
      input_lines.append(line)
      output_lines.append('0'*len(line))
    else:
      corrupted_line, corrupt_position = generator.corrupt_line(line)
      input_lines.append(corrupted_line)
      output_line = (
        '0'*(corrupt_position - 1) +
        '1' +
        '1'*(len(line) - corrupt_position)
      )
      output_lines.append(output_line)
  for file_prefix, out_lines in [('inputs', input_lines),
                                 ('outputs', output_lines)]:
    out_file = make_out_file(input_file, file_prefix,
                             version_number, corrupt_percentage)
    logging.info('Writing out to file: %s', out_file)
    with open(out_file, 'w') as f:
      for line in out_lines:
        line = line.replace('\n', '')
        if file_prefix == 'inputs':
          line = map_input_line_to_numbers(line)
        f.write(f'{line}\n')


if __name__ == '__main__':
  finalize_dataset(0.5, version_number='0.0.1')
