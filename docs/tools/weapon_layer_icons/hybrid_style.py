"""Offline candidate: JAZZ layout/tone with a soft union silhouette.

Effect recipe adapted from the user-supplied gen_weapon_icons.py (rato/ToG).
No capture, segmentation or per-component tone remapping is imported.
The caller must composite native layers before applying this effect.
"""
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
from icon_layout import fit_body


def hybrid(source, size, *, sharpen=False):
    body = fit_body(source, size)
    scale = size[1] / 110
    if sharpen:
        rgb = body.convert('RGB').filter(ImageFilter.UnsharpMask(
            radius=scale, percent=45, threshold=1))
        body = Image.merge('RGBA', (*rgb.split(), body.getchannel('A')))
    rgba = np.asarray(body).astype(np.float64)
    alpha = rgba[..., 3] / 255
    silhouette = ndimage.binary_dilation(alpha > .5, iterations=max(1, round(scale)))
    glow = ndimage.gaussian_filter(np.maximum(silhouette, alpha),
                                  sigma=3.2 * scale, mode='constant') * .9
    # Keep existing body placement; fade faint tails before the fixed canvas edge.
    y, x = np.indices(alpha.shape)
    edge = np.minimum.reduce((x, y, size[0] - 1 - x, size[1] - 1 - y))
    glow *= np.clip(edge / (2 * scale), 0, 1)
    out_alpha = alpha + glow * (1 - alpha)
    color = (rgba[..., :3] * alpha[..., None] +
             3 * (glow * (1 - alpha))[..., None]) / np.maximum(out_alpha[..., None], 1e-8)
    result = np.dstack((color, out_alpha * 255))
    return Image.fromarray(np.round(np.clip(result, 0, 255)).astype(np.uint8), 'RGBA')
