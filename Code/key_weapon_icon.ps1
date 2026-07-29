# JAZZ-UI-001: key magenta bake backdrop to alpha; grade; fit into slot.
# Magenta (not olive): olive #504633 collides with wood/metal and eats the weapon.
param(
  [Parameter(Mandatory = $true)][string]$Path,
  [string]$OutPath = "",
  [double]$Compress = 0.57,
  [int]$OutW = 512,
  [int]$OutH = 256,
  [string]$OkPath = "",
  [Parameter(ValueFromRemainingArguments = $true)][string[]]$Ignored
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$drawing = [System.Drawing.Bitmap].Assembly.Location

if (-not $OutPath) { $OutPath = $Path }

if (-not ('JazzWeaponIconKeyV8' -as [type])) {
  Add-Type -ReferencedAssemblies @($drawing) -TypeDefinition @'
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;

public static class JazzWeaponIconKeyV8 {
  static float MagScore(byte r, byte g, byte b) {
    int excess = Math.Min(r, b) - g;
    if (excess <= 0) return 0f;
    float chroma = excess / 255f;
    float magentaBias = Math.Min(r, b) / 255f;
    return excess + chroma * 40f * magentaBias;
  }

  static bool IsSunHotspot(byte r, byte g, byte b) {
    int maxc = Math.Max(r, Math.Max(g, b));
    int minc = Math.Min(r, Math.Min(g, b));
    if (maxc < 110 || maxc > 235) return false;
    float sat = maxc == 0 ? 0f : (maxc - minc) / (float)maxc;
    return sat < 0.10f;
  }

  // Magenta / alpha only — never key charcoal (super-black weapons were eaten).
  static bool IsBgSeed(byte r, byte g, byte b, byte a) {
    if (a < 8) return true;
    return MagScore(r, g, b) >= 16f;
  }

  static bool IsBgSoft(byte r, byte g, byte b, byte a) {
    if (a < 20) return true;
    if (MagScore(r, g, b) >= 7f) return true;
    if (IsSunHotspot(r, g, b)) return true;
    // Magenta spill into near-black fringe only (not solid weapon metal).
    if (r <= 14 && g <= 14 && b <= 14 && MagScore(r, g, b) >= 2f) return true;
    return false;
  }

  static void Grade(ref int r, ref int g, ref int b, double compress) {
    // Lift shadows a bit so matte-black guns keep edge detail.
    double lum = (r + g + b) / 765.0;
    double f = compress + (1.0 - compress) * (1.0 - lum) * 0.22;
    r = Math.Min(255, (int)(r * f));
    g = Math.Min(255, (int)(g * f));
    b = Math.Min(255, (int)(b * f));
    int maxc = Math.Max(r, Math.Max(g, b));
    if (maxc > 190) {
      double t = (maxc - 190) / 65.0;
      double hf = 1.0 - 0.28 * Math.Min(1.0, t);
      r = Math.Min(255, (int)(r * hf));
      g = Math.Min(255, (int)(g * hf));
      b = Math.Min(255, (int)(b * hf));
    }
  }

  public static Bitmap Process(Bitmap src, double compress, int outW, int outH) {
    int w = src.Width, h = src.Height;
    var work = new Bitmap(w, h, PixelFormat.Format32bppArgb);
    using (var gr = Graphics.FromImage(work)) {
      gr.CompositingMode = CompositingMode.SourceCopy;
      gr.DrawImageUnscaled(src, 0, 0);
    }

    var data = work.LockBits(new Rectangle(0, 0, w, h), ImageLockMode.ReadWrite, PixelFormat.Format32bppArgb);
    int stride = Math.Abs(data.Stride);
    byte[] px = new byte[stride * h];
    Marshal.Copy(data.Scan0, px, 0, px.Length);

    bool[] bg = new bool[w * h];
    var q = new Queue<int>();
    Action<int, int> seed = (x, y) => {
      if (x < 0 || y < 0 || x >= w || y >= h) return;
      int i = y * w + x;
      if (bg[i]) return;
      int o = y * stride + x * 4;
      if (!IsBgSeed(px[o + 2], px[o + 1], px[o], px[o + 3])) return;
      bg[i] = true;
      q.Enqueue(i);
    };
    for (int x = 0; x < w; x++) { seed(x, 0); seed(x, h - 1); }
    for (int y = 0; y < h; y++) { seed(0, y); seed(w - 1, y); }

    int[] dx = { 1, -1, 0, 0, 1, 1, -1, -1 };
    int[] dy = { 0, 0, 1, -1, 1, -1, 1, -1 };
    while (q.Count > 0) {
      int i = q.Dequeue();
      int x = i % w, y = i / w;
      for (int k = 0; k < 8; k++) {
        int nx = x + dx[k], ny = y + dy[k];
        if (nx < 0 || ny < 0 || nx >= w || ny >= h) continue;
        int ni = ny * w + nx;
        if (bg[ni]) continue;
        int o = ny * stride + nx * 4;
        if (!IsBgSoft(px[o + 2], px[o + 1], px[o], px[o + 3])) continue;
        bg[ni] = true;
        q.Enqueue(ni);
      }
    }

    for (int y = 0; y < h; y++) {
      for (int x = 0; x < w; x++) {
        int i = y * w + x;
        if (bg[i]) continue;
        int o = y * stride + x * 4;
        byte r = px[o + 2], g = px[o + 1], b = px[o];
        if (MagScore(r, g, b) >= 36f || IsSunHotspot(r, g, b)) bg[i] = true;
      }
    }

    // Interior magenta through frame-stock holes.
    for (int y = 0; y < h; y++) {
      for (int x = 0; x < w; x++) {
        int i = y * w + x;
        if (bg[i]) continue;
        int o = y * stride + x * 4;
        if (MagScore(px[o + 2], px[o + 1], px[o]) < 12f) continue;
        bg[i] = true;
        q.Enqueue(i);
      }
    }
    while (q.Count > 0) {
      int i = q.Dequeue();
      int x = i % w, y = i / w;
      for (int k = 0; k < 8; k++) {
        int nx = x + dx[k], ny = y + dy[k];
        if (nx < 0 || ny < 0 || nx >= w || ny >= h) continue;
        int ni = ny * w + nx;
        if (bg[ni]) continue;
        int o = ny * stride + nx * 4;
        if (!IsBgSoft(px[o + 2], px[o + 1], px[o], px[o + 3])) continue;
        bg[ni] = true;
        q.Enqueue(ni);
      }
    }

    int minX = w, minY = h, maxX = -1, maxY = -1;
    for (int y = 0; y < h; y++) {
      for (int x = 0; x < w; x++) {
        int i = y * w + x;
        int o = y * stride + x * 4;
        if (bg[i]) {
          px[o] = 0; px[o + 1] = 0; px[o + 2] = 0; px[o + 3] = 0;
          continue;
        }
        int r = px[o + 2], g = px[o + 1], b = px[o];
        int excess = Math.Min(r, b) - g;
        if (excess > 6) {
          r = Math.Min(r, g + 10);
          b = Math.Min(b, g + 10);
        }
        Grade(ref r, ref g, ref b, compress);
        px[o + 2] = (byte)r; px[o + 1] = (byte)g; px[o] = (byte)b;
        if (x < minX) minX = x;
        if (y < minY) minY = y;
        if (x > maxX) maxX = x;
        if (y > maxY) maxY = y;
      }
    }

    Marshal.Copy(px, 0, data.Scan0, px.Length);
    work.UnlockBits(data);

    if (maxX < minX) {
      var empty = new Bitmap(outW, outH, PixelFormat.Format32bppArgb);
      work.Dispose();
      return empty;
    }

    int padX = Math.Max(1, (maxX - minX + 1) / 50);
    int padY = Math.Max(1, (maxY - minY + 1) / 40);
    minX = Math.Max(0, minX - padX);
    minY = Math.Max(0, minY - padY);
    maxX = Math.Min(w - 1, maxX + padX);
    maxY = Math.Min(h - 1, maxY + padY);
    int cw = maxX - minX + 1;
    int ch = maxY - minY + 1;

    var cropped = work.Clone(new Rectangle(minX, minY, cw, ch), PixelFormat.Format32bppArgb);
    work.Dispose();

    var dst = new Bitmap(outW, outH, PixelFormat.Format32bppArgb);
    using (var g = Graphics.FromImage(dst)) {
      g.Clear(Color.Transparent);
      g.CompositingMode = CompositingMode.SourceOver;
      g.InterpolationMode = InterpolationMode.HighQualityBicubic;
      g.PixelOffsetMode = PixelOffsetMode.HighQuality;
      double fit = 0.88;
      double scale = Math.Min((double)outW / cw, (double)outH / ch) * fit;
      int dw = Math.Max(1, (int)Math.Round(cw * scale));
      int dh = Math.Max(1, (int)Math.Round(ch * scale));
      int ox = (outW - dw) / 2;
      int oy = (outH - dh) / 2;
      g.DrawImage(cropped, new Rectangle(ox, oy, dw, dh));
    }
    cropped.Dispose();
    return dst;
  }

  public static string CornerAlpha(Bitmap img) {
    Color c = img.GetPixel(0, 0);
    Color d = img.GetPixel(img.Width - 1, img.Height - 1);
    return string.Format("a00={0} a11={1} size={2}x{3}", c.A, d.A, img.Width, img.Height);
  }
}
'@
}

if (-not (Test-Path -LiteralPath $Path)) { throw "Source not found: $Path" }

$src = [System.Drawing.Bitmap]::FromFile($Path)
Write-Output ("SRC corner RGB={0},{1},{2} A={3} size={4}x{5}" -f $src.GetPixel(0,0).R, $src.GetPixel(0,0).G, $src.GetPixel(0,0).B, $src.GetPixel(0,0).A, $src.Width, $src.Height)
$out = [JazzWeaponIconKeyV8]::Process($src, $Compress, $OutW, $OutH)
$src.Dispose()

$outDir = Split-Path -Parent $OutPath
if ($outDir -and -not (Test-Path -LiteralPath $outDir)) {
  New-Item -ItemType Directory -Force -Path $outDir | Out-Null
}

$tmp = $OutPath + '.tmp.png'
$out.Save($tmp, [System.Drawing.Imaging.ImageFormat]::Png)
Write-Output ("OUT {0}" -f [JazzWeaponIconKeyV8]::CornerAlpha($out))
$a00 = $out.GetPixel(0, 0).A
$out.Dispose()
Move-Item -LiteralPath $tmp -Destination $OutPath -Force

if ($a00 -gt 40) {
  throw "chroma key failed: corner still opaque (A=$a00)"
}

if ($OkPath) {
  Set-Content -LiteralPath $OkPath -Value "OK transparent corners" -Encoding ASCII
}

if ($OutPath -ne $Path -and (Test-Path -LiteralPath $Path)) {
  Remove-Item -LiteralPath $Path -Force -ErrorAction SilentlyContinue
}

Write-Output "OK"
