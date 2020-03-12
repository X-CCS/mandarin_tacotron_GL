import tensorflow as tf


# Default hyperparameters:
hparams = tf.contrib.training.HParams(
  # Comma-separated list of cleaners to run on text prior to training and eval. For non-English
  # text, you may want to use "basic_cleaners" or "transliteration_cleaners" See TRAINING_DATA.md.
  cleaners='basic_cleaners',

  # Audio:
  num_mels=80,
  num_freq=2049,
  sample_rate=48000,
  frame_length_ms=50,
  frame_shift_ms=12.5,
  preemphasis=0.97,
  min_level_db=-100,
  ref_level_db=20,
  max_frame_num=1000,
  max_abs_value = 4,
  fmin = 125, # for male, set 55
  fmax = 7600, # for male, set 3600

  # Model:
  outputs_per_step=5,
  embed_depth=512,
  prenet_depths=[256, 256],
  encoder_depth=256,
  postnet_depth=512,
  attention_depth=128,
  decoder_depth=1024,

  # Training:
  batch_size=32,
  adam_beta1=0.9,
  adam_beta2=0.999,
  initial_learning_rate=0.001,
  decay_learning_rate=True,
  use_cmudict=False,  # Use CMUDict during training to learn pronunciation of ARPAbet phonemes

  # Eval:
  max_iters=300,
  griffin_lim_iters=60,
  power=1.2,              # Power to raise magnitudes to prior to Griffin-Lim
)


def hparams_debug_string():
  values = hparams.values()
  hp = ['  %s: %s' % (name, values[name]) for name in sorted(values)]
  return 'Hyperparameters:\n' + '\n'.join(hp)
