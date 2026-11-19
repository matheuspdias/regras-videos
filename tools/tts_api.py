"""Roda DENTRO da GitHub Action `tts`: gera cada fala pela API do HeyGen (POST /v3/models/audio/tts, heygen-voice-1),
salva media/<ep>/audio/NNN.mp3 e acrescenta a linha em episodes/<ep>/tts.tsv.
Precisa do segredo HEYGEN_API_KEY. Erros vão para tts_out/<ep>_erros.txt (e a Action termina com falha)."""
import json
import os
import sys
import time
import urllib.error
import urllib.request

KEY = os.environ['HEYGEN_API_KEY']
API = 'https://api.heygen.com/v3/models/audio/tts'   # HeyGen Voice 1 (o mesmo modelo que a assinatura usava)


def speech(voice, text):
    body = json.dumps({'text': text, 'voice_id': voice, 'model': 'heygen-voice-1', 'language': 'pt',
                       'output_format': {'encoding': 'mp3', 'sample_rate_hertz': 44100, 'bitrate_bps': 128000}}).encode()
    for attempt in range(5):
        req = urllib.request.Request(API, data=body, method='POST',
                                     headers={'X-Api-Key': KEY, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                j = json.load(r); return j.get('data', j)
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors='replace')[:400]
            if e.code in (429, 500, 502, 503, 504) and attempt < 4:
                time.sleep(5 * (attempt + 1)); continue
            raise RuntimeError(f'HTTP {e.code}: {msg}')
        except urllib.error.URLError as e:
            if attempt < 4:
                time.sleep(5); continue
            raise


def main():
    errors = []
    for f in sorted(os.listdir('tts_in')):
        if not f.endswith('.json'):
            continue
        spec = json.load(open(f'tts_in/{f}'))
        ep = spec['ep']
        os.makedirs(f'media/{ep}/audio', exist_ok=True)
        os.makedirs(f'episodes/{ep}', exist_ok=True)
        tsv = f'episodes/{ep}/tts.tsv'
        done = set()
        if os.path.exists(tsv):
            done = {int(r.split('\t')[0]) for r in open(tsv) if r.strip()}
        from concurrent.futures import ThreadPoolExecutor
        import threading
        lock = threading.Lock()

        def one(j):
            i = j['i']
            try:
                d = speech(j['voice'], j['text'])
                dest = f'media/{ep}/audio/{i:03d}.mp3'
                for attempt in range(4):
                    try:
                        urllib.request.urlretrieve(d['audio_url'], dest); break
                    except Exception:
                        time.sleep(3)
                with lock:
                    with open(tsv, 'a') as fh:
                        fh.write(f"{i}\t{j['voice']}\t{d.get('request_id', 'api')}\t{d['duration']}\n")
                    print('ok', ep, i, round(d['duration'], 2), flush=True)
            except Exception as e:
                with lock:
                    errors.append(f'{ep} fala {i} ({j["voice"]}): {e}')
                    print('ERRO', errors[-1], flush=True)

        with ThreadPoolExecutor(max_workers=4) as ex:
            list(ex.map(one, [j for j in spec['jobs'] if j['i'] not in done]))
        if not errors:
            os.remove(f'tts_in/{f}')
    if errors:
        os.makedirs('tts_out', exist_ok=True)
        with open(f'tts_out/erros_{int(time.time())}.txt', 'w') as fh:
            fh.write('\n'.join(errors) + '\n')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
