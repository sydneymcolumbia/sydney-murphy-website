"""Weekly investing post generator.

Usage:  python3 scripts/new_post.py spec.json
The JSON spec has keys: slug, iso (YYYY-MM-DD), date ("Sep 28, 2026"), tag, cover_kicker,
title, dek, card_blurb, sections, verdict.  `sections` is a list of [h2_or_null, blocks];
each block is a paragraph string, or ["ul", [items]], or ["levels", "Table title", [[label, value], ...]].
`verdict` is a list of 2 paragraphs (the second wrapped in <strong>Playbook: ...</strong>).
Writes posts/<slug>.html, images/post-<slug>.jpg (dark card cover), and prepends the card to investing-update.html.
Requires Pillow (pip install pillow)."""
import os, re, html, textwrap
from PIL import Image, ImageDraw, ImageFont
import pathlib
SITE=str(pathlib.Path(__file__).resolve().parent.parent)
TPL=f'{SITE}/posts/hike-is-live-fed-week-ahead-september-2026.html'

def font(size, bold=True):
    cands=(['/System/Library/Fonts/Supplemental/Georgia Bold.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf','/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf'] if bold else ['/System/Library/Fonts/Supplemental/Georgia.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf','/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf'])+['/System/Library/Fonts/Helvetica.ttc','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    for p in cands:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except Exception: pass
    return ImageFont.load_default()

def cover(slug, kicker, title):
    W,H=1600,900; im=Image.new('RGB',(W,H),(13,13,13)); d=ImageDraw.Draw(im)
    for i in range(0,W+H,90): d.line([(i,0),(i-H,H)],fill=(20,20,20),width=40)
    d.rectangle([0,0,W,H],outline=(42,42,42),width=6); d.rectangle([90,120,150,128],fill=(201,168,76))
    d.text((90,150),kicker.upper(),font=font(34,False),fill=(201,168,76))
    lines=textwrap.wrap(title,width=32)[:5]; fs=78 if len(lines)<=4 else 66; f=font(fs); y=230
    for ln in lines: d.text((90,y),ln,font=f,fill=(240,240,240)); y+=int(fs*1.23)
    d.text((90,H-110),"SYDNEY MURPHY  ·  INVESTING",font=font(28,False),fill=(136,136,136))
    im.save(f'{SITE}/images/post-{slug}.jpg',quality=82,optimize=True)

def body_html(sections, verdict):
    out=''
    for h2, blocks in sections:
        if h2: out+=f'      <h2>{h2}</h2>\n'
        for b in blocks:
            if isinstance(b,tuple) and b[0]=='ul':
                out+='      <ul>\n'+''.join(f'        <li>{x}</li>\n' for x in b[1])+'      </ul>\n'
            elif isinstance(b,tuple) and b[0]=='levels':
                out+=f'      <div class="key-levels">\n        <h3>{b[1]}</h3>\n        <table>\n'+''.join(f'          <tr><td>{k}</td><td>{v}</td></tr>\n' for k,v in b[2])+'        </table>\n      </div>\n'
            else: out+=f'      <p>{b}</p>\n'
    out+='      <div class="verdict-box">\n        <h3>My Take</h3>\n'+''.join(f'        <p>{p}</p>\n' for p in verdict)+'      </div>\n'
    return out

def build_post(s):
    t=open(TPL).read(); slug=s['slug']; T=s['title']; esc=lambda x: html.escape(x,quote=True)
    cover(slug, s['cover_kicker'], T)
    old_title='Payrolls Just Tripled Expectations. A September Hike Is Live. Here Is the Hike-Proof Playbook.'
    t=t.replace(f'<title>{old_title} — Sydney Murphy</title>', f'<title>{T} — Sydney Murphy</title>')
    t=re.sub(r'<meta name="description" content="[^"]*"', f'<meta name="description" content="{esc(s["dek"])}"', t)
    t=re.sub(r'<meta property="og:title" content="[^"]*"', f'<meta property="og:title" content="{esc(T)}"', t)
    t=re.sub(r'<meta property="og:description" content="[^"]*"', f'<meta property="og:description" content="{esc(s["dek"])}"', t)
    t=t.replace('content="2026-09-07"', f'content="{s["iso"]}"')
    t=re.sub(r'<span class="post-tag">[^<]*</span>\n        <span class="post-date">[^<]*</span>', f'<span class="post-tag">{s["tag"]}</span>\n        <span class="post-date">{s["date"]}</span>', t)
    t=t.replace(f'<h1>{old_title}</h1>', f'<h1>{T}</h1>')
    t=re.sub(r'(<p style="color: var\(--text-muted\); font-size: 0.95rem; line-height: 1.7; margin-top: 1rem;">)[^<]*(</p>)', lambda m: m.group(1)+s['dek']+m.group(2), t)
    t=re.sub(r'<div class="post-cover"><img src="[^"]*" alt="[^"]*" /></div>', f'<div class="post-cover"><img src="../images/post-{slug}.jpg" alt="{esc(T)}" /></div>', t)
    a=t.index('    <div class="post-body">\n')+len('    <div class="post-body">\n'); b=t.index('\n      <div class="post-disclaimer">')
    t=t[:a]+body_html(s['sections'], s['verdict'])+t[b:]
    open(f'{SITE}/posts/{slug}.html','w').write(t)
    card=f'''        <div class="post-card">
          <img class="post-card-img" src="images/post-{slug}.jpg" alt="{esc(T)}" />
          <div class="post-card-body">
            <div class="post-meta">
              <span class="post-tag">{s['tag']}</span>
              <span class="post-date">{s['date']}</span>
            </div>
            <h3>{T}</h3>
            <p>{s['card_blurb']}</p>
            <a class="post-read-more" href="posts/{slug}.html">Read More &rarr;</a>
          </div>
        </div>

'''
    p=f'{SITE}/investing-update.html'; h=open(p).read(); m='      <div class="posts-grid">\n\n'
    assert m in h; open(p,'w').write(h.replace(m, m+card, 1))
    return slug

if __name__=='__main__':
    import json, sys
    spec=json.load(open(sys.argv[1]))
    spec['sections']=[(h, [tuple(b) if isinstance(b,list) else b for b in blocks]) for h,blocks in spec['sections']]
    spec['sections']=[(h,[('levels',b[1],[tuple(r) for r in b[2]]) if isinstance(b,tuple) and b[0]=='levels' else b for b in blocks]) for h,blocks in spec['sections']]
    print('built', build_post(spec))
