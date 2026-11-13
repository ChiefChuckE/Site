# MAYDAY YouTube thumbnail maker. Usage: python3 make_thumb.py DAY "BIG ORANGE WORDS" "WHITE WORDS" [out.png]
# Needs: playwright (chromium), fonts from npm @fontsource/anton + @fontsource/inter (set FONTS dir below).
import sys, os
from playwright.sync_api import sync_playwright
HERE=os.path.dirname(os.path.abspath(__file__))
FONTS=os.environ.get("FONTS","/tmp/claude-0/fonts")
day,l1,l2=sys.argv[1],sys.argv[2],sys.argv[3]
out=sys.argv[4] if len(sys.argv)>4 else f"MAYDAY-Day-{int(day):02d}-thumbnail.png"
s=open(f"{HERE}/thumbnail.dc.html").read()
body=s[s.index("</helmet>")+9:s.index("</x-dc>")]
body=body.replace("/_blob/e0a3b37637dd29a7e07c58f9046fa054",f"file://{HERE}/thumb_base.jpg").replace("/_blob/386752d85e8665f7058e7ad43a62dde2",f"file://{HERE}/logo_badge.png")
body=body.replace("{{day}}",day).replace("{{line1}}",l1).replace("{{line2}}",l2)
css=f"""@font-face{{font-family:Anton;src:url(file://{FONTS}/fontsource-anton-5.3.0/files/anton-latin-400-normal.woff2)}}
@font-face{{font-family:Inter;font-weight:900;src:url(file://{FONTS}/fontsource-inter-5.3.0/files/inter-latin-900-normal.woff2)}}body{{margin:0}}"""
open(f"{HERE}/_render.html","w").write(f"<html><head><style>{css}</style></head><body>{body}</body></html>")
with sync_playwright() as p:
  b=p.chromium.launch(); pg=b.new_page(viewport={"width":1280,"height":720})
  pg.goto(f"file://{HERE}/_render.html"); pg.wait_for_timeout(800)
  pg.evaluate("""()=>{document.querySelectorAll('[style*=nowrap]').forEach(el=>{let fs=parseFloat(getComputedStyle(el).fontSize);while(el.getBoundingClientRect().right>700&&fs>40){fs-=2;el.style.fontSize=fs+'px';}})}""")
  pg.screenshot(path=out); b.close()
print(out)
