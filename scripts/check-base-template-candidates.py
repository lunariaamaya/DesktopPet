"""Validate reference immutability and index reference artwork with user status.

File checks do not prove anatomical accuracy, visual fidelity, view consistency,
layer separation or rigging. This index must never be used as a runtime model.
"""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageChops

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'assets/characters/base-templates'
GENERATED=Path('C:/Users/HP/.codex/generated_images/01a188e5-a910-7c63-bb00-10491ab286cc')
ITEMS=[('base-a','魔法师','base-a-mage/v01','base-a-mage-mannequin-v01.png',
        'exec-689fb20c-c50f-4f10-acb3-b03acc0c363b.png'),
       ('base-b','弓箭手','base-b-archer/v01','base-b-archer-mannequin-v01.png',
        'exec-a38901f6-5f28-4060-8306-dc899f4ff423.png')]

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    references=json.loads((BASE/'reference-inventory.json').read_text(encoding='utf-8'))['references']
    for item in references:
        current=item.get('currentSource',item['source'])
        assert sha(ROOT/current)==item['sha256'],current
    additional=[]
    for inventory in sorted(BASE.glob('*/v*/reference-inventory.json')):
        for item in json.loads(inventory.read_text(encoding='utf-8')).get('sources',[]):
            source=ROOT/item['source']
            assert sha(source)==item['sha256'],item['source']
            with Image.open(source) as image:
                assert (image.width,image.height)==(item['width'],item['height'])
            additional.append(item)
    records=[]
    for tid,label,folder,name,source_name in ITEMS:
        path=BASE/folder/name
        with Image.open(path) as image:
            image.load();assert image.width>image.height and image.width>=1024
            record={'templateId':tid,'displayName':label,'revision':'draft-01',
                'artifact':path.relative_to(BASE).as_posix(),'sha256':sha(path),
                'width':image.width,'height':image.height,'mode':image.mode,
                'prompt':folder+'/mannequin-prompt.txt','method':'built-in image_gen',
                'referenceImagesUsedForGeneration':[],
                'kind':'independent_mechanical_proportion_sketch',
                'approval':'not_reviewed','referenceFit':'not_verified',
                'layers':None,'rig':None,'runtimeLoadable':False,
                'manualReview':{'views':'front, left side, back',
                    'limits':['Mechanical sketch, not a human base or exact reconstruction',
                              'Proportions not approved; do not proceed to binding',
                              'No PSD/CMO3/MOC3 or animation delivered']}}
        # Built-in generation originals are kept; no pixel postprocessing.
        if (GENERATED/source_name).exists():assert sha(GENERATED/source_name)==record['sha256']
        records.append(record)
    for candidate_file in sorted(BASE.glob('*/v*/candidate.json')):
        record=json.loads(candidate_file.read_text(encoding='utf-8'))
        assert record['templateId'] in {'base-a','base-b'}
        path=BASE/record['artifact'];assert sha(path)==record['sha256']
        with Image.open(path) as image:
            image.load();assert (image.width,image.height)==(record['width'],record['height'])
        original=GENERATED/record['sourceBuiltinFilename']
        processing=record.get('postprocessing')
        if processing:
            source=BASE/processing['sourceArtifact']
            mask_path=BASE/processing['maskArtifact']
            assert sha(source)==processing['sourceSha256']
            assert sha(mask_path)==processing['maskSha256']
            if original.exists():assert sha(original)==sha(source)
            with Image.open(source) as source_image,Image.open(path) as output_image,Image.open(mask_path) as mask_image:
                mask=mask_image.convert('L')
                assert mask.size==source_image.size==output_image.size
                bbox=mask.getbbox();bounds=processing['allowedBoundsXYXY']
                assert bbox and bbox[0]>=bounds[0] and bbox[1]>=bounds[1] and bbox[2]<=bounds[2] and bbox[3]<=bounds[3]
                difference=ImageChops.difference(source_image.convert('RGB'),output_image.convert('RGB'))
                difference.paste((0,0,0),mask=mask.point(lambda p:255 if p>0 else 0))
                assert difference.getbbox() is None,'Pixels changed outside processing mask'
                assert ImageChops.difference(source_image.convert('RGBA').getchannel('A'),output_image.convert('RGBA').getchannel('A')).getbbox() is None
            script=(ROOT/processing['script']).read_text(encoding='utf-8').replace('\r\n','\n')
            assert hashlib.sha256(script.encode('utf-8')).hexdigest()==processing['scriptSha256NormalizedLF']
        elif original.exists():assert sha(original)==record['sha256']
        assert record['approval'] in {'not_reviewed','revision_requested','rejected','approved_reference'} and record['rig'] is None and not record['runtimeLoadable']
        if record['approval']=='approved_reference':
            evidence=record['userApproval']
            assert evidence['scope']=='front_static_reference' and evidence['quote'] and evidence['date']
        for source,digest in record.get('sourceHashes',{}).items():
            assert sha(ROOT/source)==digest,source
        records.append(record)
    approved={'base-a':None,'base-b':None}
    for record in records:
        if record['approval']=='approved_reference':
            approved[record['templateId']]={key:record[key] for key in ('revision','artifact','sha256')}
            approved[record['templateId']]['scope']='front_static_reference_only'
    for path in sorted(BASE.glob('*/baseline.json')):
        baseline=json.loads(path.read_text(encoding='utf-8'))
        selected=approved[baseline['templateId']]
        assert selected and all(baseline[key]==selected[key] for key in ('revision','artifact','sha256'))
        assert sha(BASE/baseline['artifact'])==baseline['sha256']
        assert baseline['scope']=='front_static_reference_only'
        assert baseline['userApproval']['quote']
        assert baseline['rig'] is None and not baseline['runtimeLoadable']
        selected['baselineSpecification']=path.relative_to(BASE).as_posix()
    skill_package=ROOT/'skills/character-reference-to-turnaround/references/cases/desktop-pet-base-templates'
    skill_references=json.loads((skill_package/'baselines.json').read_text(encoding='utf-8'))['templates']
    assert {item['templateId'] for item in skill_references}=={'base-a','base-b'}
    for item in skill_references:
        selected=approved[item['templateId']]
        assert selected and selected['revision']==item['revision'] and selected['sha256']==item['sha256']
        assert sha(ROOT/item['sourceProjectPath'])==sha(skill_package/item['image'])==item['sha256']
        with Image.open(skill_package/item['image']) as image:
            assert image.size==(item['width'],item['height'])
    (BASE/'candidate-index.json').write_text(json.dumps({'date':'2026-11-09',
        'updatedOn':'2026-11-10',
        'kind':'work_in_progress_index_not_runtime_manifest','approvedBaselines':approved,
        'candidates':records},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (BASE/'file-check.json').write_text(json.dumps({'sourceReferences':len(references),
        'additionalReferencesChecked':len(additional),'allAdditionalReferenceHashesUnchanged':True,
        'allOriginalHashesUnchanged':True,'candidateCount':len(records),
        'approvedFrontReferenceCount':sum(record['approval']=='approved_reference' for record in records),
        'generatedFilesCopiedWithoutPixelChanges':not any(record.get('postprocessing') for record in records),
        'postprocessedReferenceCount':sum(bool(record.get('postprocessing')) for record in records),
        'postprocessedOutputsPreserveOutsideMask':True,
        'approvedSkillReferenceCopiesChecked':len(skill_references),
        'allApprovedSkillReferenceHashesMatch':True,
        'notChecked':['reference fidelity','anatomy','view registration','layering','rigging','animation']},
        indent=2)+'\n',encoding='utf-8')
    print(f'{len(references)} original and {len(additional)} additional references unchanged; {len(records)} PNG references across 2 template IDs; approved current baselines: '+str({key:value["revision"] if value else None for key,value in approved.items()})+'; no rig claimed')

if __name__=='__main__':main()
