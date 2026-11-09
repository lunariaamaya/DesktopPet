"""Read-only inventory of the user-supplied A/B base reference images."""
from pathlib import Path
import hashlib,json
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/characters/base-templates/reference-inventory.json'
GROUPS=[('base-a','魔法师'),('base-b','弓箭手')]

def main():
    records=[]
    for template_id,label in GROUPS:
        folder=ROOT/'素体参考图'/label
        for path in sorted(folder.glob('*.png')):
            with Image.open(path) as image:
                records.append({'templateId':template_id,'label':label,'source':path.relative_to(ROOT).as_posix(),
                    'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                    'width':image.width,'height':image.height,'mode':image.mode,
                    'review':'visually_inspected','limitations':['Low-resolution game/pixel image',
                    'Pose, hairstyle and/or equipment obscure body landmarks; not an exact body recovery source']})
    assert len([r for r in records if r['templateId']=='base-a'])==8
    assert len([r for r in records if r['templateId']=='base-b'])==9
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps({'date':'2026-11-09','references':records},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for item in records:print(item['source'],item['width'],item['height'])

if __name__=='__main__':main()
