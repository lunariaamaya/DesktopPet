"""Record the new covered-reference attempt; never sends generation requests."""
from pathlib import Path
import argparse,hashlib,json,shutil
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/characters/base-templates/base-a-mage/v02'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--generated-image',type=Path,help='Record an actual built-in image_gen output; never generates an image')
    args=parser.parse_args()
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
    log=OUT/'attempt.json'
    if log.exists():
        existing=json.loads(log.read_text(encoding='utf-8'))
        assert existing['promptFileSha256']==result['promptFileSha256'],'Prompt changed; use a new revision'
        assert [(r['source'],r['sha256']) for r in existing['references']]==[(r['source'],r['sha256']) for r in records]
        result=existing  # Preserve actual generation history on later checks.
    if args.generated_image:
        source=args.generated_image.resolve();assert source.is_file()
        target=OUT/'base-a-mage-covered-front-v02.png'
        if target.exists():assert sha(target)==sha(source),'Refusing to replace a different candidate'
        else:shutil.copy2(source,target)
        assert sha(target)==sha(source)
        with Image.open(target) as im:
            im.load();width,height=im.size;mode=im.mode
            assert height>width and width>=1024
        if not any(a.get('sha256')==sha(target) for a in result['attempts']):
            result['attempts'].append({'attempt':len(result['attempts'])+1,'status':'generated',
                'output':target.name,'sha256':sha(target),
                'retry':'User requested retry after checking network; same prompt and same three references'})
        result.update({'safetyDecision':'no_separate_verdict_exposed_image_returned',
            'generationStatus':'image_received','candidateImage':target.name,'approval':'not_reviewed',
            'conclusion':'This exact fully clothed request produced an image; do not infer hidden thresholds, exact reconstruction, layering or rigging.'})
        candidate={'templateId':'base-a','displayName':'魔法师','revision':'draft-02',
            'artifact':target.relative_to(OUT.parents[1]).as_posix(),'sha256':sha(target),
            'width':width,'height':height,'mode':mode,
            'prompt':'base-a-mage/v02/prompt.txt','method':'built-in image_gen',
            'referenceImagesUsedForGeneration':[r['source'] for r in records if r['usedAsGenerationReference']],
            'kind':'covered_2d_reference_candidate','approval':'not_reviewed','referenceFit':'not_verified',
            'layers':None,'rig':None,'runtimeLoadable':False,'sourceBuiltinFilename':source.name,
            'manualReview':{'views':'front only','coverage':'opaque high-neck long-sleeve full-length neutral base clothing',
                'limits':['Static composite PNG, not PSD/CMO3/MOC3 or animation',
                          'Proportions, face, shoulder and hip silhouette require user review',
                          'Hidden structure is inferred from small posed game references',
                          'Do not interpret one successful request as a general moderation boundary']}}
        candidate_path=OUT/'candidate.json'
        if candidate_path.exists():
            previous=json.loads(candidate_path.read_text(encoding='utf-8'))
            assert previous['sha256']==candidate['sha256']
            for field in ['approval','userFeedback']:
                if field in previous:candidate[field]=previous[field]
            result['approval']=candidate['approval']
        candidate_path.write_text(json.dumps(candidate,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    log.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f"7 new references and 17 archive hashes verified; attempts={len(result['attempts'])}; {result['generationStatus']}")

if __name__=='__main__':main()
