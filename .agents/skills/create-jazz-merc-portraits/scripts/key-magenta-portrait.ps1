# Key magenta chroma to transparent PNG (JA3 merc portraits)
param(
  [Parameter(Mandatory = $true)][string]$Source,
  [Parameter(Mandatory = $true)][string]$OutFull,
  [Parameter(Mandatory = $true)][string]$OutSized,
  [Parameter(Mandatory = $true)][ValidateSet(300, 2000)][int]$Size
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$drawing = [System.Drawing.Bitmap].Assembly.Location

if (-not ('JazzMagentaKeyV5' -as [type])) {
  Add-Type -ReferencedAssemblies @($drawing) -TypeDefinition @'
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Imaging;
using System.Drawing.Drawing2D;
using System.Runtime.InteropServices;

public static class JazzMagentaKeyV5 {
  static float Mag(byte r, byte g, byte b) {
    float m = Math.Min(r, b) - g;
    return m <= 0 ? 0f : m * (Math.Min(r, b) / 255f);
  }

  public static Bitmap Key(Bitmap src) {
    int w = src.Width, h = src.Height;
    var work = new Bitmap(w, h, PixelFormat.Format32bppArgb);
    using (var gr = Graphics.FromImage(work)) {
      gr.CompositingMode = CompositingMode.SourceCopy;
      gr.DrawImageUnscaled(src, 0, 0);
    }
    var data = work.LockBits(new Rectangle(0,0,w,h), ImageLockMode.ReadWrite, PixelFormat.Format32bppArgb);
    int stride = Math.Abs(data.Stride);
    byte[] px = new byte[stride * h];
    Marshal.Copy(data.Scan0, px, 0, px.Length);

    const float hard = 26f, soft = 3f;
    bool[] bg = new bool[w * h];
    var q = new Queue<int>();
    Action<int,int> seed = (x,y) => {
      if (x<0||y<0||x>=w||y>=h) return;
      int i=y*w+x; if (bg[i]) return;
      int o=y*stride+x*4;
      if (Mag(px[o+2],px[o+1],px[o]) < hard) return;
      bg[i]=true; q.Enqueue(i);
    };
    for (int x=0;x<w;x++){ seed(x,0); seed(x,h-1);} for(int y=0;y<h;y++){ seed(0,y); seed(w-1,y);}
    int[] dx={1,-1,0,0,1,1,-1,-1}; int[] dy={0,0,1,-1,1,-1,1,-1};
    while (q.Count>0) {
      int i=q.Dequeue(); int x=i%w,y=i/w;
      for (int k=0;k<8;k++) {
        int nx=x+dx[k], ny=y+dy[k];
        if (nx<0||ny<0||nx>=w||ny>=h) continue;
        int ni=ny*w+nx; if (bg[ni]) continue;
        int o=ny*stride+nx*4;
        if (Mag(px[o+2],px[o+1],px[o]) < soft) continue;
        bg[ni]=true; q.Enqueue(ni);
      }
    }
    for (int y=0;y<h;y++) for (int x=0;x<w;x++) {
      int i=y*w+x; if (bg[i]) continue;
      int o=y*stride+x*4;
      if (Mag(px[o+2],px[o+1],px[o]) >= hard) bg[i]=true;
    }

    bool[] dil = (bool[])bg.Clone();
    for (int y=1;y<h-1;y++) for (int x=1;x<w-1;x++) {
      int i=y*w+x; if (bg[i]) continue;
      bool near=false;
      for (int k=0;k<8;k++) if (bg[(y+dy[k])*w+(x+dx[k])]) { near=true; break; }
      if (!near) continue;
      int o=y*stride+x*4;
      int r=px[o+2], g=px[o+1], b=px[o];
      int maxc=Math.Max(r, Math.Max(g,b));
      float m=Mag((byte)r,(byte)g,(byte)b);
      int excess=Math.Min(r,b)-g;
      if (maxc >= 70 && (m >= 8 || excess >= 18)) dil[i]=true;
      if (maxc >= 160 && excess >= 8) dil[i]=true;
    }
    bg = dil;

    int[] dist = new int[w*h];
    for (int i=0;i<dist.Length;i++) dist[i]=bg[i]?0:9999;
    var dq=new Queue<int>();
    for (int i=0;i<bg.Length;i++) if (bg[i]) dq.Enqueue(i);
    while (dq.Count>0) {
      int i=dq.Dequeue(); int x=i%w,y=i/w; int d=dist[i];
      if (d>=4) continue;
      for (int k=0;k<8;k++) {
        int nx=x+dx[k], ny=y+dy[k];
        if (nx<0||ny<0||nx>=w||ny>=h) continue;
        int ni=ny*w+nx;
        if (dist[ni]<=d+1) continue;
        dist[ni]=d+1; dq.Enqueue(ni);
      }
    }

    for (int y=0;y<h;y++) for (int x=0;x<w;x++) {
      int i=y*w+x; int o=y*stride+x*4;
      if (bg[i]) { px[o]=0; px[o+1]=0; px[o+2]=0; px[o+3]=0; continue; }
      int d=dist[i];
      if (d>4) continue;
      int r=px[o+2], g=px[o+1], b=px[o];
      int maxc=Math.Max(r, Math.Max(g,b));
      int excess=Math.Min(r,b)-g;

      if (maxc < 85) {
        if (excess > 0) {
          r = Math.Min(r, g + 8);
          b = Math.Min(b, g + 8);
          if (Math.Min(r,b) - g > 4) { r = (r + g) / 2; b = (b + g) / 2; }
          px[o+2]=(byte)r; px[o]=(byte)b;
        }
        continue;
      }

      if (excess > 0) {
        float str = 1f - d/4f;
        r = (int)(r*(1-str) + Math.Min(r,g)*str);
        b = (int)(b*(1-str) + Math.Min(b,g)*str);
        r = Math.Min(r, g + 10);
        b = Math.Min(b, g + 10);
        px[o+2]=(byte)Math.Max(0,Math.Min(255,r));
        px[o]=(byte)Math.Max(0,Math.Min(255,b));
      }

      float m = Mag(px[o+2], px[o+1], px[o]);
      excess = Math.Min(px[o+2], px[o]) - px[o+1];
      float fade = 1f;
      if (m > soft) fade *= 1f - Math.Min(1f, (m-soft)/Math.Max(1f, hard-soft));
      if (excess > 12) fade *= 1f - Math.Min(0.85f, (excess-12)/40f);
      if (maxc > 140 && d <= 2) fade *= 0.35f;
      if (d <= 1 && (m > 10 || excess > 15 || maxc > 170)) fade = 0f;
      px[o+3] = (byte)Math.Min(px[o+3], Math.Max(0, (int)(fade*255)));
      if (px[o+3] < 12) { px[o]=0; px[o+1]=0; px[o+2]=0; px[o+3]=0; }
    }

    Marshal.Copy(px,0,data.Scan0,px.Length);
    work.UnlockBits(data);
    return work;
  }

  public static Bitmap ResizeHQ(Bitmap src, int tw, int th) {
    var dst = new Bitmap(tw, th, PixelFormat.Format32bppArgb);
    using (var g = Graphics.FromImage(dst)) {
      g.Clear(Color.Transparent);
      g.CompositingMode = CompositingMode.SourceCopy;
      g.InterpolationMode = InterpolationMode.HighQualityBicubic;
      g.PixelOffsetMode = PixelOffsetMode.HighQuality;
      g.DrawImage(src, new Rectangle(0,0,tw,th));
    }
    return dst;
  }

  public static string Stats(Bitmap img) {
    int op=0,tr=0,mag=0,cast=0;
    for(int y=0;y<img.Height;y+=2) for(int x=0;x<img.Width;x+=2){
      Color p=img.GetPixel(x,y);
      if(p.A<16){tr++;continue;}
      op++;
      if(p.R>180&&p.B>180&&p.G<100) mag++;
      if(Math.Min(p.R,p.B)-p.G > 18 && p.A>40) cast++;
    }
    return string.Format("cornerA={0} opaque~={1} trans~={2} magLeft~={3} magCast~={4}", img.GetPixel(0,0).A,op,tr,mag,cast);
  }
}
'@
}

if (-not (Test-Path -LiteralPath $Source)) { throw "Source not found: $Source" }
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $OutFull) | Out-Null
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $OutSized) | Out-Null

$raw = New-Object System.Drawing.Bitmap $Source
Write-Output ("SRC corner RGB={0},{1},{2}" -f $raw.GetPixel(0,0).R, $raw.GetPixel(0,0).G, $raw.GetPixel(0,0).B)
$keyed = [JazzMagentaKeyV5]::Key($raw)
$raw.Dispose()
$keyed.Save($OutFull, [System.Drawing.Imaging.ImageFormat]::Png)
Write-Output ("FULL {0}" -f [JazzMagentaKeyV5]::Stats($keyed))
$sized = [JazzMagentaKeyV5]::ResizeHQ($keyed, $Size, $Size)
$keyed.Dispose()
$sized.Save($OutSized, [System.Drawing.Imaging.ImageFormat]::Png)
Write-Output ("OUT  {0}" -f [JazzMagentaKeyV5]::Stats($sized))
$sized.Dispose()
