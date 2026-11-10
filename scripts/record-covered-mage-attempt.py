"""Record the new covered-reference attempt; never sends generation requests."""
from pathlib import Path
import hashlib,json
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/characters/base-templates/base-a-mage/v02'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    # Verify the archive relocation against the already committed old snapshot
    # BEFORE refreshing paths. A moved image must not silently become a new one.
    old=json.loads((OUT.parents[1]/'reference-inventory.json').read_text(encoding='utf-8'))
    for ref in old['references']:
        original=ROOT/ref['source'];current=original.parent/'穿太少了'/original.name
        assert current.is_file() and sha(current)==ref['sha256'],str(current)
    folder=ROOT/'素体参考图/魔法师/新素体参考图'
    records=[]
    used={'新魔法师素体1.png','新魔法师素体3.png','新魔法师素体5.png'}
    for p in sorted(folder.glob('*.png')):
        with Image.open(p) as image:
            records.append({'source':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size,
                'width':image.width,'height':image.height,'visuallyInspected':True,
                'usedAsGenerationReference':p.name in used})
    assert len(records)==7
    result={'date':'2026-11-10','templateId':'base-a','label':'魔法师',
        'scope':'One fully clothed, opaque neutral-unitard front-view 2D reference candidate',
        'references':records,'prompt':'prompt.txt','promptFileSha256':sha(OUT/'prompt.txt'),
        'method':'built-in image_gen','transparentBackground':False,
        'attempts':[
            {'attempt':1,'status':'transport_error','error':'image generation failed: connection failed: error sending request','output':None},
            {'attempt':2,'status':'transport_error','error':'image generation failed: connection failed: error sending request','output':None,
             'retry':'Same prompt and same three references; no coverage or wording changes'}],
        'safetyDecision':'not_available','generationStatus':'no_result_received',
        'candidateImage':None,'rig':None,'approval':'not_applicable_no_image',
        'conclusion':'Network/transport failure cannot establish whether image moderation accepted or rejected the request.',
        'oldReferenceRelocation':{'verifiedImages':len(old['references']),'allHashesUnchanged':True,
             'currentArchiveDirectory':'穿太少了'}}
    (OUT/'attempt.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('7 new references indexed; 17 archived reference hashes unchanged; 2 transport errors, no safety decision')

if __name__=='__main__':main()
