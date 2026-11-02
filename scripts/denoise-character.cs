using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;

public static class CharacterDenoise
{
    // Windows-only deterministic RGB bilateral filtering; never synthesizes geometry.
    public static string Run(string input, string output, string skinReference)
    {
        if (System.IO.File.Exists(output)) throw new InvalidOperationException("Output already exists.");
        using (var loaded = new Bitmap(input))
        using (var image = new Bitmap(loaded.Width, loaded.Height, PixelFormat.Format32bppArgb))
        {
            using (var g = Graphics.FromImage(image)) g.DrawImageUnscaled(loaded, 0, 0);
            int w = image.Width, h = image.Height, n = w * h;
            var rect = new Rectangle(0, 0, w, h);
            var bits = image.LockBits(rect, ImageLockMode.ReadWrite, PixelFormat.Format32bppArgb);
            if (bits.Stride != w * 4) { image.UnlockBits(bits); throw new InvalidOperationException("Unexpected stride."); }
            byte[] original = new byte[n * 4];
            Marshal.Copy(bits.Scan0, original, 0, original.Length);
            bool[] background = new bool[n];
            int[] queue = new int[n]; int head=0, tail=0;
            Action<int> visit = p => {
                if (background[p]) return;
                int k = p * 4;
                int min = Math.Min(original[k], Math.Min(original[k+1], original[k+2]));
                int max = Math.Max(original[k], Math.Max(original[k+1], original[k+2]));
                if (min >= 250 && max - min <= 2 && original[k+3] == 255) {
                    background[p] = true; queue[tail++]=p;
                }
            };
            for (int x=0; x<w; x++) { visit(x); visit((h-1)*w+x); }
            for (int y=0; y<h; y++) { visit(y*w); visit(y*w+w-1); }
            while (head<tail) {
                int p=queue[head++], x=p%w, y=p/w;
                if(x>0) visit(p-1); if(x+1<w) visit(p+1);
                if(y>0) visit(p-w); if(y+1<h) visit(p+w);
            }
            // Keep high-contrast linework and anti-aliased boundaries exactly intact.
            bool[] protectedEdge = new bool[n]; int edgeCount=0, bgCount=0;
            for (int y=1;y<h-1;y++) for(int x=1;x<w-1;x++) {
                int p=y*w+x, k=p*4;
                if(background[p]) continue;
                bool edge=false;
                for(int dy=-1;dy<=1;dy++) for(int dx=-1;dx<=1;dx++) {
                    int j=((y+dy)*w+x+dx)*4;
                    for(int c=0;c<3;c++) if(Math.Abs(original[k+c]-original[j+c])>28) edge=true;
                }
                protectedEdge[p]=edge; if(edge) edgeCount++;
            }
            byte[] filtered = Pass(original, w, h, background, protectedEdge, 3, 1.5, 7.0);
            filtered = Pass(filtered, w, h, background, protectedEdge, 5, 2.5, 10.0);
            long absolute=0; int changed=0; double maxDelta=0;
            for(int p=0;p<n;p++) {
                int k=p*4;
                if(background[p]) { bgCount++; filtered[k]=filtered[k+1]=filtered[k+2]=255; }
                if(protectedEdge[p]) for(int c=0;c<3;c++) filtered[k+c]=original[k+c];
                filtered[k+3]=original[k+3];
                bool different=false;
                for(int c=0;c<3;c++) {
                    int d=Math.Abs(filtered[k+c]-original[k+c]);
                    absolute+=d; maxDelta=Math.Max(maxDelta,d); if(d>0)different=true;
                }
                if(different) changed++;
            }
            int skinPixels=0; double deltaR=0,deltaG=0,deltaB=0;
            if (!String.IsNullOrEmpty(skinReference)) {
                if(w!=1536 || h!=1024) throw new InvalidOperationException("Skin ROIs require 1536x1024 layout.");
                using(var reference = new Bitmap(skinReference)) {
                    if(reference.Width!=w || reference.Height!=h) throw new InvalidOperationException("Reference layout mismatch.");
                    double[] target=new double[3], source=new double[3]; int count=0;
                    for(int y=840;y<876;y++)for(int x=732;x<739;x++) {
                        var c=reference.GetPixel(x,y);int k=(y*w+x)*4;
                        target[0]+=c.B;target[1]+=c.G;target[2]+=c.R;
                        for(int j=0;j<3;j++)source[j]+=filtered[k+j];count++;
                    }
                    double[] delta=new double[3];
                    for(int j=0;j<3;j++) delta[j]=(target[j]-source[j])/count;
                    deltaB=delta[0];deltaG=delta[1];deltaR=delta[2];
                    // Layout-specific skin ROIs exclude dress trim, headwear, gems and bows.
                    int[,] boxes={{190,140,435,302},{140,385,248,570},{393,385,480,570},
                        {250,790,370,980},{650,140,810,301},{710,385,770,570},
                        {650,790,770,980},{1060,480,1130,565},{1350,480,1410,565},{1170,790,1290,980}};
                    for(int p=0;p<n;p++) {
                        if(background[p])continue;int x=p%w,y=p/w;bool inside=false;
                        for(int a=0;a<boxes.GetLength(0);a++)if(x>=boxes[a,0]&&y>=boxes[a,1]&&x<boxes[a,2]&&y<boxes[a,3])inside=true;
                        if(!inside)continue;int k=p*4;
                        double r=original[k+2],g=original[k+1],b=original[k];
                        double weight=Smooth((r-g-3)/5)*Smooth((r-b-5)/8)*Smooth((g-150)/25)*Smooth((b-140)/25);
                        if(weight<=0)continue;skinPixels++;
                        for(int j=0;j<3;j++)filtered[k+j]=(byte)Math.Clamp(Math.Round(filtered[k+j]+delta[j]*weight),0,255);
                    }
                }
            }
            Marshal.Copy(filtered, 0, bits.Scan0, filtered.Length);
            image.UnlockBits(bits);
            image.Save(output, ImageFormat.Png);
            return "{\"width\":"+w+",\"height\":"+h+",\"backgroundPixels\":"+bgCount+
                ",\"protectedEdgePixels\":"+edgeCount+",\"changedPixels\":"+changed+
                ",\"meanAbsoluteChannelChange\":"+(absolute/(n*3.0)).ToString("F6",System.Globalization.CultureInfo.InvariantCulture)+
                ",\"maxChannelChangeBeforeSkin\":"+maxDelta+
                ",\"skinPixels\":"+skinPixels+",\"skinDeltaRGB\":["+
                deltaR.ToString("F4",System.Globalization.CultureInfo.InvariantCulture)+","+
                deltaG.ToString("F4",System.Globalization.CultureInfo.InvariantCulture)+","+
                deltaB.ToString("F4",System.Globalization.CultureInfo.InvariantCulture)+"]}";
        }
    }
    static double Smooth(double t) { t=Math.Clamp(t,0,1);return t*t*(3-2*t); }
    static byte[] Pass(byte[] src,int w,int h,bool[] bg,bool[] edge,int radius,double spatial,double range)
    {
        byte[] dst=(byte[])src.Clone(); int side=radius*2+1;
        double[] weights=new double[side*side];
        for(int dy=-radius;dy<=radius;dy++) for(int dx=-radius;dx<=radius;dx++)
            weights[(dy+radius)*side+dx+radius]=Math.Exp(-(dx*dx+dy*dy)/(2*spatial*spatial));
        // LUT removes millions of expensive exp evaluations.
        double[] colorWeight=new double[195076];
        for(int i=0;i<colorWeight.Length;i++) colorWeight[i]=Math.Exp(-i/(6*range*range));
        System.Threading.Tasks.Parallel.For(radius,h-radius,y=>{
            for(int x=radius;x<w-radius;x++) {
                int p=y*w+x,k=p*4;if(bg[p]||edge[p])continue;
                double sum=0,b=0,g=0,r=0;
                for(int dy=-radius;dy<=radius;dy++) for(int dx=-radius;dx<=radius;dx++) {
                    int q=(y+dy)*w+x+dx;if(bg[q])continue;int j=q*4;
                    int db=src[j]-src[k],dg=src[j+1]-src[k+1],dr=src[j+2]-src[k+2];
                    double weight=weights[(dy+radius)*side+dx+radius]*colorWeight[db*db+dg*dg+dr*dr];
                    sum+=weight;b+=weight*src[j];g+=weight*src[j+1];r+=weight*src[j+2];
                }
                if(sum>0) {dst[k]=(byte)Math.Round(b/sum);dst[k+1]=(byte)Math.Round(g/sum);dst[k+2]=(byte)Math.Round(r/sum);}
            }
        });
        return dst;
    }
}
