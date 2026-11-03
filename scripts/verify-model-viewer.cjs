const fs=require('node:fs');
const path=require('node:path');
const {pathToFileURL}=require('node:url');
const {chromium}=require(process.argv[2] || 'playwright');
(async()=>{
  const folder=path.resolve(__dirname,'../assets/characters/first-character/models/v01');
  const browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true,args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']});
  try{
    const page=await browser.newPage({viewport:{width:1200,height:900}});
    const errors=[],external=[];
    page.on('pageerror',e=>errors.push(String(e)));
    page.on('request',r=>{if(/^https?:/.test(r.url()))external.push(r.url());});
    await page.goto(pathToFileURL(path.join(folder,'viewer.html')).href);
    await page.waitForFunction(()=>document.querySelector('#status').textContent.includes('个三角形'));
    const settle=()=>page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
    await settle();
    await page.screenshot({path:path.join(folder,'viewer-preview.png'),fullPage:true});
    for(const angle of ['1.5707963','3.1415926','0']){
      await page.locator(`[data-angle="${angle}"]`).click();await settle();
    }
    await page.locator('#hair').click();await settle();
    await page.locator('#hair').click();await settle();
    const state=await page.evaluate(()=>({status:document.querySelector('#status').textContent,webglError:document.querySelector('canvas').getContext('webgl2').getError()}));
    const result={...state,pageErrors:errors,externalRequests:external.length,angleButtonsTested:3,hairToggleTested:true};
    fs.writeFileSync(path.join(folder,'viewer-validation.json'),JSON.stringify(result,null,2));
    console.log(JSON.stringify(result));
    if(errors.length||external.length||state.webglError!==0)process.exitCode=1;
  } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
