from absl import flags

HETERO_ARRAYS = flags.DEFINE_bool(
    'experimental_hetero_arrays',
    False,
    'Support heterogeneous arrays.')
