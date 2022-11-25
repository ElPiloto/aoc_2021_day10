import collections


FILENAME = 'aoc_input.txt'
OPENING_CHARS = [ '{', '[', '(', '<']
CLOSING_MATCHES = {
  '}': '{',
  ']': '[',
  '>': '<',
  ')': '(',
}

POINTS = {
  ')': 3,
  ']': 57,
  '}': 1197,
  '>': 25137,
  '': 0
}


def check_line(line: str, should_print: bool = True) -> str:
  opened_chars = collections.deque()
  for idx, cur_char in enumerate(line):
    if cur_char in OPENING_CHARS:
      opened_chars.append(cur_char)
    else:
      try:
        last_opened_char = opened_chars.pop()
      except IndexError:
        last_opened_char = 'NO_MATCH'
      if CLOSING_MATCHES[cur_char] != last_opened_char:
        if should_print:
          print(f'Found error at position {idx} on char {cur_char}.')
        return cur_char
  return ''

if __name__ == '__main__':
  with open(FILENAME, 'r') as f:
    lines = f.readlines()

  count = 0
  for line in lines:
    count += POINTS[check_line(line.strip('\n'), False)]
  print(count)
