import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
def regions(im):
    """Return (kind, [boxes]) for one 1080x1920 RGB frame: boxes to blur around the LEADERSHIP tape."""
    a = np.asarray(im).astype(int); Y0, X0 = 1050, 250
    sub = a[Y0:1800, X0:1080]; R, G, B = sub[..., 0], sub[..., 1], sub[..., 2]
    yel = (R > 195) & (G > 165) & (B < 155) & (R - B > 65)
    yel = ndimage.binary_opening(yel, iterations=2)
    lab, n = ndimage.label(yel)
    if n == 0: return 'none', []
    sizes = ndimage.sum(yel, lab, range(1, n + 1)); k = int(np.argmax(sizes)) + 1; area = sizes[k - 1]
    if area < 3500: return 'none', []
    ys, xs = np.nonzero(lab == k); yx0, yx1 = np.percentile(xs, [1, 99]); yy0, yy1 = np.percentile(ys, [1, 99]); W = yx1 - yx0; H = yy1 - yy0
    full = [(X0 + yx0 - .45 * max(W, 200), Y0 + yy0 - .75 * max(W, 200), X0 + yx1 + .55 * max(W, 200), Y0 + yy1 + .6 * max(W, 200))]
    if not (area > 15000 and 170 < W < 340 and 190 < H < 440): return 'full', full
    red = (R > 165) & (G < 90) & (B < 95)
    m = np.zeros_like(red); m[int(max(0, yy0 - 10)):int(yy1), int(max(0, yx0)):int(yx1)] = True
    ry, rx = np.nonzero(red & m)
    if len(rx) < 250: return 'full', full
    ty0, ty1 = np.percentile(ry, [4, 96]); tx1 = np.percentile(rx, 98)
    if ty1 - ty0 > 0.6 * W or ty1 - ty0 < 25: return 'full', full
    L, Rr = X0 + yx0 - .22 * W, X0 + yx1 + .40 * W
    return 'exact', [(L, Y0 + ty0 - .95 * W, Rr, Y0 + ty0 - 7), (L, Y0 + ty1 + .38 * W, Rr, Y0 + ty1 + 1.3 * W), (X0 + tx1 + 7, Y0 + ty0 - .95 * W, Rr, Y0 + ty1 + 1.3 * W)]
def apply(im, boxes, r=18):
    for (a, b, c, d) in boxes:
        a, b, c, d = int(max(0, a)), int(max(0, b)), int(min(1080, c)), int(min(1920, d))
        if c - a > 4 and d - b > 4: im.paste(im.crop((a, b, c, d)).filter(ImageFilter.GaussianBlur(r)), (a, b))
    return im
if __name__ == '__main__':
    out = []; kinds = {}
    for i in range(1, 310):
        im = Image.open(f'q/dbg/{i:04d}.jpg').convert('RGB'); k, bx = regions(im); kinds[i] = k
        if i in (150, 196, 200, 206, 215, 240, 270, 285, 291, 296, 302, 308): out.append(apply(im, bx).crop((250, 1000, 1080, 1800)).resize((415, 400)))
    s = Image.new('RGB', (415 * 6, 800)); [s.paste(o, ((j % 6) * 415, (j // 6) * 400)) for j, o in enumerate(out)]; s.save('q/dbg_sheet.jpg', quality=88)
    seq = ''.join({'none': '.', 'full': 'F', 'exact': 'E'}[kinds[i]] for i in range(1, 310)); print(seq)
