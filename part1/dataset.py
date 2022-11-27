import tensorflow as tf

DEFAULT_INPUT_FILE = 'one_million_lines_v0.0.1_inputs_corrupt_50.0_percent.txt'
DEFAULT_OUTPUT_FILE = 'one_million_lines_v0.0.1_outputs_corrupt_50.0_percent.txt'

PADDING_VALUE = -1

def build_dataset(sequence_length: int = 20,
                  batch_size: int = 4):
  input_lines_ds = tf.data.TextLineDataset(filenames=[DEFAULT_INPUT_FILE])
  output_lines_ds = tf.data.TextLineDataset(filenames=[DEFAULT_OUTPUT_FILE])

  ds = tf.data.Dataset.zip((input_lines_ds, output_lines_ds))

  def _remove_lines_too_long(input_line: tf.Tensor, output_line: tf.Tensor):
    return tf.strings.length(input_line) <= sequence_length

  ds = ds.filter(_remove_lines_too_long)
  ds = ds.shuffle(buffer_size = 20)
  def _preprocess_fn(x, y):
    x = tf.strings.unicode_split(x, 'UTF-8')
    x = tf.strings.to_number(x, out_type=tf.int32)

    y = tf.strings.unicode_split(y, 'UTF-8')
    y = tf.strings.to_number(y, out_type=tf.int32)
    return x, y

  ds = ds.map(_preprocess_fn)

  ds = ds.padded_batch(batch_size,
                       padded_shapes=(sequence_length, sequence_length),
                       padding_values=(PADDING_VALUE, PADDING_VALUE))
  return ds


if __name__ == "__main__":
  ds = build_dataset(20)
  ds_iter = ds.as_numpy_iterator()
  for i in range(2000):
    example = next(ds_iter)
    __import__('pdb').set_trace()
    print(example)
