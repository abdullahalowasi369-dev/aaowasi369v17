import asyncio, json, re
from pathlib import Path
from playwright.async_api import async_playwright

ROOT=Path('/mnt/data/aaowasi369v17')
html=ROOT.joinpath('index.html').read_text()
css=ROOT.joinpath('assets/site-v17.css').read_text()
js=ROOT.joinpath('assets/app-v17.js').read_text()
html=re.sub(r'<link\s+href="/assets/site-v17\.css"\s+rel="stylesheet"\s*/>', lambda m:f'<style>{css}</style>', html, count=1)
html=re.sub(r'<script\s+defer="True"\s+src="/assets/app-v17\.js">\s*</script>', lambda m:f'<script>{js}</script>', html, count=1)

mock={"catalogVersion":"2026.08.18","dateReleased":"2026-08-18T12:00:00.0000Z","count":6,"vulnerabilities":[
{"cveID":"CVE-2026-1111","vendorProject":"Example Vendor A","product":"Gateway","vulnerabilityName":"Gateway authorization vulnerability","dateAdded":"2026-08-18","shortDescription":"A public test record used only for browser-layout QA.","requiredAction":"Apply mitigations per vendor instructions.","dueDate":"2026-08-21","knownRansomwareCampaignUse":"Unknown"},
{"cveID":"CVE-2026-2222","vendorProject":"Example Vendor B","product":"Identity Service","vulnerabilityName":"Identity service access-control vulnerability","dateAdded":"2026-08-17","shortDescription":"A public test record used only for browser-layout QA.","requiredAction":"Apply mitigations per vendor instructions.","dueDate":"2026-09-01","knownRansomwareCampaignUse":"Known"},
{"cveID":"CVE-2026-3333","vendorProject":"Example Vendor C","product":"Collaboration Suite","vulnerabilityName":"Collaboration suite vulnerability","dateAdded":"2026-08-12","shortDescription":"A public test record used only for browser-layout QA.","requiredAction":"Apply mitigations per vendor instructions.","dueDate":"2026-09-05","knownRansomwareCampaignUse":"Unknown"},
{"cveID":"CVE-2026-4444","vendorProject":"Example Vendor A","product":"Server","vulnerabilityName":"Server vulnerability","dateAdded":"2026-08-03","shortDescription":"QA.","requiredAction":"Mitigate.","dueDate":"2026-09-10","knownRansomwareCampaignUse":"Unknown"},
{"cveID":"CVE-2026-5555","vendorProject":"Example Vendor D","product":"VPN","vulnerabilityName":"VPN vulnerability","dateAdded":"2026-07-25","shortDescription":"QA.","requiredAction":"Mitigate.","dueDate":"2026-08-30","knownRansomwareCampaignUse":"Unknown"},
{"cveID":"CVE-2026-6666","vendorProject":"Example Vendor E","product":"Endpoint","vulnerabilityName":"Endpoint vulnerability","dateAdded":"2026-07-01","shortDescription":"QA.","requiredAction":"Mitigate.","dueDate":"2026-08-01","knownRansomwareCampaignUse":"Unknown"}
]}

async def rect(el):
    return await el.bounding_box() if el else None

def overlap(a,b):
    if not a or not b: return 0
    x=max(0,min(a['x']+a['width'],b['x']+b['width'])-max(a['x'],b['x']))
    y=max(0,min(a['y']+a['height'],b['y']+b['height'])-max(a['y'],b['y']))
    return round(x*y,2)

async def main():
    out=[]
    async with async_playwright() as p:
      browser=await p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
      for width,height in [(1440,1000),(1024,900),(768,900),(620,900),(540,844),(430,844),(390,844),(360,800),(320,760)]:
        page=await browser.new_page(viewport={'width':width,'height':height})
        errors=[]
        page.on('pageerror', lambda e: errors.append(str(e)))
        async def route_handler(route):
          if 'known_exploited_vulnerabilities.json' in route.request.url:
            await route.fulfill(status=200, content_type='application/json', body=json.dumps(mock))
          else:
            await route.abort()
        await page.route('**/*', route_handler)
        await page.set_content(html, wait_until='domcontentloaded')
        await page.wait_for_timeout(450)
        overflow_x=await page.evaluate('document.documentElement.scrollWidth-document.documentElement.clientWidth')
        # Governance no-click number 03.
        stage03=page.locator('[data-stage-goto="2"]')
        await stage03.dispatch_event('pointerenter', {'pointerType':'mouse'})
        await page.wait_for_timeout(80)
        gov_status=(await page.locator('[data-stage-readout]').inner_text()).strip()
        # Architecture / systems / capabilities hover.
        arch=page.locator('[data-flag-tab="1"]'); await arch.dispatch_event('pointerenter', {'pointerType':'mouse'}); await page.wait_for_timeout(50)
        arch_active=(await page.locator('[data-flag-panel="1"] h3').inner_text()).strip() if await page.locator('[data-flag-panel="1"]').evaluate('(e)=>e.classList.contains("active")') else 'FAIL'
        sys=page.locator('[data-project-filter="AI Governance"]'); await sys.dispatch_event('pointerenter', {'pointerType':'mouse'}); await page.wait_for_timeout(40)
        sys_active=await sys.get_attribute('aria-pressed')
        cap=page.locator('[data-skill-filter="Automation"]'); await cap.dispatch_event('pointerenter', {'pointerType':'mouse'}); await page.wait_for_timeout(40)
        cap_active=await cap.get_attribute('aria-pressed')
        # Known overlap guards.
        focus=await rect(page.locator('.governance-card.is-focus'))
        proof=await rect(page.locator('[data-governance-proof]'))
        controls=await rect(page.locator('.stage-controls'))
        heat_boxes=[await rect(page.locator('.heat-node').nth(i)) for i in range(await page.locator('.heat-node').count())]
        heat_overlap=sum(overlap(heat_boxes[i],heat_boxes[j]) for i in range(len(heat_boxes)) for j in range(i+1,len(heat_boxes)))
        # Table card mode: compare visible td boxes in AI table pairwise; sibling td overlap means broken layout.
        tdloc=page.locator('[data-responsive-table="3"] tbody tr:first-child td')
        tdb=[await rect(tdloc.nth(i)) for i in range(await tdloc.count())]
        table_overlap=sum(overlap(tdb[i],tdb[j]) for i in range(len(tdb)) for j in range(i+1,len(tdb)))
        # Dynamic-island icon optical center difference.
        await page.evaluate('window.scrollTo(0, document.querySelector("#architecture").offsetTop)')
        await page.wait_for_timeout(120)
        island=page.locator('[data-island]'); toggle=page.locator('[data-island-toggle]'); plus=page.locator('.island-chevron')
        tr=await rect(toggle); pr=await rect(plus)
        island_center_delta=None
        if tr and pr:
          island_center_delta=round(abs((pr['y']+pr['height']/2)-(tr['y']+tr['height']/2)),2)
        # Scroll-jump guard.
        await page.evaluate('''() => { document.documentElement.style.scrollBehavior='auto'; window.scrollTo(0, Math.min(7000, document.documentElement.scrollHeight-innerHeight-20)); }''')
        await page.wait_for_timeout(50)
        y0=await page.evaluate('scrollY'); await page.wait_for_timeout(1200); y1=await page.evaluate('scrollY')
        # Live result loaded.
        live_status=(await page.locator('[data-live-status]').inner_text()).strip()
        hidden_instruction=await page.evaluate('''() => document.body.innerText.includes('Move across categories') || document.body.innerText.includes('Glide on desktop') || document.body.innerText.includes('Integrated modules · move across') || document.body.innerText.includes('grouped swipe deck · Scroll / Swipe') || document.body.innerText.includes('Example only — demonstrates the decision lineage')''')
        contact_size=float((await page.locator('.contact-intro h2').evaluate('(e)=>getComputedStyle(e).fontSize')).replace('px',''))
        out.append({'width':width,'overflowX':overflow_x,'govStatus':gov_status,'archActive':arch_active,'systemsAI':sys_active,'capAutomation':cap_active,'govProofOverlap':overlap(focus,proof),'govControlsOverlap':overlap(focus,controls),'heatOverlapArea':heat_overlap,'tableCellOverlapArea':table_overlap,'islandIconCenterDeltaPx':island_center_delta,'scrollJumpPx':round(y1-y0,2),'liveStatus':live_status,'hiddenInstructionText':hidden_instruction,'contactTitlePx':contact_size,'errors':errors})
        # Final screenshots for representative layouts.
        if width in [1440,390]:
          await page.evaluate('window.scrollTo(0,0)'); await page.wait_for_timeout(100)
          await page.screenshot(path=str(ROOT/f'validation/v17_final_home_{width}.png'), full_page=False)
          await page.locator('[data-governance-stage]').screenshot(path=str(ROOT/f'validation/v17_final_governance_{width}.png'))
          await page.locator('#architecture').scroll_into_view_if_needed(); await page.wait_for_timeout(120)
          await page.locator('#architecture').screenshot(path=str(ROOT/f'validation/v17_final_architecture_{width}.png'))
          await page.locator('#live-risk-pulse').scroll_into_view_if_needed(); await page.wait_for_timeout(100)
          await page.locator('#live-risk-pulse').screenshot(path=str(ROOT/f'validation/v17_final_live_{width}.png'))
        await page.close()
      await browser.close()
    ROOT.joinpath('validation/browser-v17-final.json').write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))

asyncio.run(main())
