import whisperx
import torch
import gc
from utils import download

batch_size = 4
compute_type = 'int8'
device = 'gpu' if torch.cuda.is_available() else 'cpu'
print('using device:', device)

models = dict()
models['ja'] = whisperx.load_model('base', device=device, compute_type=compute_type, language='ja', download_root='./cache')
# models['en'] = whisperx.load_model('base', device=device, compute_type=compute_type, language='en', download_root='./cache')

# alinger_models = dict()
# alinger_metadata = dict()
# alinger_models['ja'], alinger_metadata['ja'] = whisperx.load_align_model(language_code='ja', device=device)

# diarizer_model = whisperx.diarize.DiarizationPipeline("pyannote/speaker-diarization-3.1", device=device, use_auth_token=)

def collect_garbage():
  gc.collect()

def transcribe(lang, audio):
  global models, batch_size
  # diarized_seg = diarizer_model(audio)

  res = models[lang].transcribe(audio, batch_size=batch_size, task='transcribe' if lang == 'en' else 'translate')
  # res = whisperx.align(res['segments'], alinger_models[lang], alinger_metadata[lang], audio, device)
  # res = whisperx.assign_word_speakers(diarized_seg, res)
  return res

if __name__ == '__main__':
  test_audios = {
    1: {
      'url': 'https://www3.nhk.or.jp/nhkworld/lesson/en/mp3/audio_lesson_01.mp3',
      'path': './cache/tests/audio_lesson_01.mp3'
    }
  }
  download(test_audios[1])
  audio = whisperx.load_audio(test_audios[1]['path'])
  result = transcribe('ja', audio)
  print(result)
  with open('./cache/tests/audio_lesson_01.json', 'w') as fp:
    import json
    json.dump(result, fp, indent=2)
