import asyncio, json, re
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path('/mnt/data/aaowasi369v17')
html=ROOT.joinpath('index.html').read_text(); css=ROOT.joinpath('assets/site-v17.css').read_text(); js=ROOT.joinpath('assets/app-v17.js').read_text()
html=re.sub(r'<link\s+href="/assets/site-v17\.css"\s+rel="stylesheet"\s*/>',lambda m:f'<style>{css}</style>',html,1)
html=re.sub(r'<script\s+defer="True"\s+src="/assets/app-v17\.js">\s*</script>',lambda m:f'<script>{js}</script>',html,1)
mock={"catalogVersion":"2026.08.18","dateReleased":"2026-08-18T12:00:00.0000Z","count":3,"vulnerabilities":[
{"cveID":"CVE-2026-1111","vendorProject":"Example Vendor A","product":"Gateway","vulnerabilityName":"Gateway authorization vulnerability","dateAdded":"2026-08-18","shortDescription":"Layout example for the customization guide.","dueDate":"2026-08-21","knownRansomwareCampaignUse":"Unknown"},
{"cveID":"CVE-2026-2222","vendorProject":"Example Vendor B","product":"Identity Service","vulnerabilityName":"Identity service access-control vulnerability","dateAdded":"2026-08-17","shortDescription":"Layout example for the customization guide.","dueDate":"2026-09-01","knownRansomwareCampaignUse":"Known"},
{"cveID":"CVE-2026-3333","vendorProject":"Example Vendor C","product":"Collaboration Suite","vulnerabilityName":"Collaboration suite vulnerability","dateAdded":"2026-08-12","shortDescription":"Layout example for the customization guide.","dueDate":"2026-09-05","knownRansomwareCampaignUse":"Unknown"}]}
async def make(page,width,height):
    await page.set_viewport_size({'width':width,'height':height})
    await page.set_content(html, wait_until='domcontentloaded'); await page.wait_for_timeout(350)
    await page.add_style_tag(content='.dynamic-island,.skip-link,.executive-nav{display:none!important}')
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    page=await b.new_page()
    async def rh(route):
      if 'known_exploited_vulnerabilities.json' in route.request.url: await route.fulfill(status=200,content_type='application/json',body=json.dumps(mock))
      else: await route.abort()
    await page.route('**/*',rh)
    await make(page,390,844)
    await page.locator('.portfolio-snapshot').screenshot(path=str(ROOT/'validation/doc_governance_390.png'))
    await page.locator('[data-flag-tab="2"]').dispatch_event('pointerenter', {'pointerType':'mouse'})
    await page.wait_for_timeout(80)
    await page.locator('[data-responsive-table="3"]').screenshot(path=str(ROOT/'validation/doc_ai_table_390.png'))
    await page.locator('.heatmap-panel').screenshot(path=str(ROOT/'validation/doc_ai_matrix_390.png'))
    await page.locator('#live-risk-pulse').screenshot(path=str(ROOT/'validation/doc_live_390.png'))
    await page.locator('#contact-cta').screenshot(path=str(ROOT/'validation/doc_contact_390.png'))
    await make(page,1440,1000)
    await page.locator('#architecture').screenshot(path=str(ROOT/'validation/doc_architecture_1440.png'))
    await b.close()
asyncio.run(main())
