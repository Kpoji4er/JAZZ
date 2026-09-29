"""Deterministic output layout for the native live-capture processing pipeline."""
from pathlib import Path
import json
from functools import lru_cache
import numpy as np
from PIL import Image, ImageFilter

ROOT=Path(__file__).resolve().parents[3]
RECIPE={'version':3,'color':'original-icon per-weapon monotonic luminance curve and saturation',
        'padding_large':8,'padding_small':5,'outline_px':2}

def target_size(entry):
    path=str(entry.get('icon',''))
    if path.startswith('Mod/e6L4ECj/'):
        p=ROOT/path.removeprefix('Mod/e6L4ECj/')
        if p.is_file():
            with Image.open(p) as im:
                if im.size in [(324,165),(162,110)]: return im.size
    return (162,110) if entry['parents'][0] in ['Pistol','Autopistol','Revolver','FlareGun'] else (324,165)

@lru_cache(maxsize=1)
def color_profiles():
    return json.loads((ROOT/'docs/design/weapon-layer-icons/live/color-profiles.json').read_text(encoding='utf-8'))

def colorize(source,weapon,profiles=None):
    """Apply the fixed family tone without changing alpha or shared coordinates."""
    rgba=source.convert('RGBA')
    a=np.asarray(rgba).copy()
    rgb=a[...,:3].astype(np.float32)/255
    lum=rgb[...,0:1]*.2126+rgb[...,1:2]*.7152+rgb[...,2:3]*.0722
    profiles=profiles or color_profiles()
    profile=profiles['profiles'].get(weapon,profiles['fallback'])
    rgb=lum+(rgb-lum)*profile['saturation']
    mapped=np.interp(lum,profile['source_luma'],profile['target_luma'])
    rgb=rgb*(mapped/np.maximum(lum,.0001))
    a[...,:3]=np.round(np.clip(rgb,0,1)*255).astype(np.uint8)
    rgba=Image.fromarray(a)
    return rgba

def render(source,size,weapon):
    return fit(colorize(source,weapon),size)


def fit(source,size):
    """Fit and outline already graded layers without applying the tone twice."""
    rgba=source.convert('RGBA')
    bounds=rgba.getchannel('A').point(lambda a:255 if a>16 else 0).getbbox()
    if not bounds: raise ValueError('Empty weapon silhouette')
    x0,y0,x1,y1=bounds
    rgba=rgba.crop((max(0,x0-2),max(0,y0-2),min(rgba.width,x1+2),min(rgba.height,y1+2)))
    pad=RECIPE['padding_small'] if size[0]==162 else RECIPE['padding_large']
    scale=min((size[0]-2*pad)/rgba.width,(size[1]-2*pad)/rgba.height)
    rgba=rgba.resize((max(1,round(rgba.width*scale)),max(1,round(rgba.height*scale))),Image.Resampling.LANCZOS)
    canvas=Image.new('RGBA',size)
    canvas.alpha_composite(rgba,((size[0]-rgba.width)//2,(size[1]-rgba.height)//2))
    outline=Image.new('RGBA',size,(5,6,7,0))
    outline.putalpha(canvas.getchannel('A').filter(ImageFilter.MaxFilter(5)))
    outline.alpha_composite(canvas)
    return outline
