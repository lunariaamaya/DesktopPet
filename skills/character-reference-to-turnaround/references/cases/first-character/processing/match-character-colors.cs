using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;
using System.Text;

public static class CharacterColorMatch
{
    // Layout-specific material masks. Coordinates belong to the approved 1536x1024 sheet.
    static int[,] skin={{190,140,435,302},{140,385,248,570},{393,385,480,570},
        {250,790,370,980},{650,140,810,301},{710,385,770,570},
        {650,790,770,980},{1060,480,1130,565},{1350,480,1410,565},{1170,790,1290,980}};
    static int[,] head={{170,48,269,226},{367,46,447,228},{737,48,858,238},
        {1104,49,1206,231},{1266,48,1374,232}};
    static int[,] cat={{214,12,275,102},{363,12,416,102},{718,13,791,113},
        {1139,14,1200,108},{1274,14,1329,109}};
    static int[,] bows={{48,617,161,760},{868,615,975,764},{1325,622,1455,765}};
    static int[,] trim={{144,715,485,763},{583,715,883,765},{1055,715,1412,764}};
    static int[][] tails={
        new[]{225,517,193,536,148,563,109,594,88,625,88,645,107,650,123,612,166,580,213,556},
        new[]{88,684,118,683,139,710,128,737,109,751,94,729},
        new[]{796,479,827,493,869,535,900,579,918,619,934,672,941,726,929,751,906,752,898,719,903,670,897,627,877,584,845,551,809,527},
        new[]{1238,479,1272,498,1310,530,1352,566,1386,603,1408,647,1418,701,1401,737,1375,748,1361,725,1381,694,1384,656,1363,621,1327,591,1282,557,1248,528}};
    static bool In(int x,int y,int[,] boxes) {
        for(int i=0;i<boxes.GetLength(0);i++) if(x>=boxes[i,0]&&y>=boxes[i,1]&&x<boxes[i,2]&&y<boxes[i,3])return true;
        return false;
    }
    static bool Tail(int x,int y) {
        foreach(var p in tails) {bool inside=false;int n=p.Length/2;
            for(int i=0,j=n-1;i<n;j=i++)if((p[i*2+1]>y)!=(p[j*2+1]>y)&&x<(p[j*2]-p[i*2])*(y-p[i*2+1])/(double)(p[j*2+1]-p[i*2+1])+p[i*2])inside=!inside;
            if(inside)return true;
        } return false;
    }
    static double Smooth(double t) { t=Math.Clamp(t,0,1);return t*t*(3-2*t); }
    static double L(double r,double g,double b) {return .2126*r+.7152*g+.0722*b;}
    static double Warm(double r,double g,double b) {
        return Smooth((r-g-2)/6)*Smooth((r-b-4)/8)*Smooth((g-145)/30)*Smooth((b-140)/30)*Smooth((65-(r-g))/10);
    }
    static double Purple(double r,double g,double b) {
        return Smooth((b-g-10)/14)*Smooth((r-g-3)/12)*Smooth((238-L(r,g,b))/25);
    }
    static double Neutral(double r,double g,double b) {
        double y=L(r,g,b),spread=Math.Max(r,Math.Max(g,b))-Math.Min(r,Math.Min(g,b));
        return Smooth((y-165)/30)*Smooth((65-spread)/25)*Smooth((255-y)/20);
    }
    // Returns one material index; no spatial resampling is ever performed.
    static int Class(int x,int y,double r,double g,double b,out double weight) {
        weight=0;
        if(In(x,y,cat)) {
            weight=Warm(r,g,b);if(weight>.01)return 2;
            weight=Neutral(r,g,b);if(weight>.01)return 3;
        }
        if(In(x,y,skin)) {weight=Warm(r,g,b);if(weight>.01)return 0;}
        if(In(x,y,head)||In(x,y,bows)) {weight=Purple(r,g,b);if(weight>.01)return 1;}
        if(In(x,y,trim)) {weight=Smooth((r-g-2)/8)*Smooth((r-b-3)/8)*Smooth((g-70)/30);if(weight>.01)return 5;}
        if(Tail(x,y)) {weight=Neutral(r,g,b);if(weight>.01)return 4;}
        weight=0;return -1;
    }
    static byte[] Read(Bitmap bitmap) {
        var rect=new Rectangle(0,0,bitmap.Width,bitmap.Height);
        var bits=bitmap.LockBits(rect,ImageLockMode.ReadOnly,PixelFormat.Format32bppArgb);
        if(bits.Stride!=bitmap.Width*4)throw new InvalidOperationException("Unexpected stride.");
        byte[] data=new byte[bitmap.Width*bitmap.Height*4];Marshal.Copy(bits.Scan0,data,0,data.Length);bitmap.UnlockBits(bits);return data;
    }
    static Bitmap Load(string path) {
        using(var input=new Bitmap(path)) {var result=new Bitmap(input.Width,input.Height,PixelFormat.Format32bppArgb);
            using(var g=Graphics.FromImage(result))g.DrawImageUnscaled(input,0,0);return result;}
    }
    public static string Run(string input,string reference,string output,string maskPath) {
        if(System.IO.File.Exists(output)||System.IO.File.Exists(maskPath))throw new InvalidOperationException("Refusing to overwrite existing output.");
        using(var image=Load(input)) using(var guide=Load(reference)) {
            int w=image.Width,h=image.Height,n=w*h;
            if(w!=1536||h!=1024||guide.Width!=w||guide.Height!=h)throw new InvalidOperationException("Requires approved 1536x1024 layout.");
            byte[] src=Read(image),refdata=Read(guide),dst=(byte[])src.Clone(),mask=new byte[n*4];
            // Derive material chroma differences from robust selected color families, not copied shapes.
            double[,] sums=new double[6,6];
            for(int p=0;p<n;p++)for(int which=0;which<2;which++) {
                byte[] data=which==0?src:refdata;int k=p*4,x=p%w,y=p/w;
                double b=data[k],g=data[k+1],r=data[k+2],weight;int c=Class(x,y,r,g,b,out weight);
                // Calf is a stable unoccluded skin color anchor for both layouts.
                if(c==0 && !(x>=728&&x<745&&y>=825&&y<878))continue;
                if(c<0||weight<.85)continue;
                // Match cat-white and tail-white shadows, not nearly white highlights.
                double l=L(r,g,b);if((c==3||c==4)&&(l<195||l>242))continue;
                int j=which*3;sums[c,j]+=r-l;sums[c,j+1]+=b-l;sums[c,j+2]++;
            }
            double[,] delta=new double[6,2];double[,] similarity=new double[6,2];
            for(int c=0;c<6;c++) {
                if(sums[c,2]<10||sums[c,5]<10)throw new InvalidOperationException("Insufficient samples for material "+c);
                for(int j=0;j<2;j++)delta[c,j]=Math.Clamp(sums[c,3+j]/sums[c,5]-sums[c,j]/sums[c,2],-20,20);
                double su=sums[c,0]/sums[c,2],sv=sums[c,1]/sums[c,2],tu=sums[c,3]/sums[c,5],tv=sums[c,4]/sums[c,5];
                double divisor=su*su+sv*sv;
                similarity[c,0]=divisor>1?(tu*su+tv*sv)/divisor:1;
                similarity[c,1]=divisor>1?(tv*su-tu*sv)/divisor:0;
            }
            int[] changed=new int[6];double sumLum=0,maxLum=0;int unchangedBackground=0;
            for(int p=0;p<n;p++) {
                int k=p*4;double b=src[k],g=src[k+1],r=src[k+2],weight;
                int c=Class(p%w,p/w,r,g,b,out weight);
                mask[k+3]=255;
                if(c<0) {if(r==255&&g==255&&b==255)unchangedBackground++;continue;}
                double dr=delta[c,0]*weight,db=delta[c,1]*weight;
                if(c==1||c==5) {
                    double l=L(r,g,b),u=r-l,v=b-l;
                    dr=(similarity[c,0]*u-similarity[c,1]*v-u)*weight;
                    db=(similarity[c,1]*u+similarity[c,0]*v-v)*weight;
                }
                double dg=-(.2126*dr+.0722*db)/.7152;
                // Scale all deltas together at gamut boundary to preserve encoded luma.
                double scale=1;double[] old={b,g,r},d={db,dg,dr};
                for(int j=0;j<3;j++)if(d[j]>0)scale=Math.Min(scale,(255-old[j])/d[j]);else if(d[j]<0)scale=Math.Min(scale,-old[j]/d[j]);
                for(int j=0;j<3;j++)dst[k+j]=(byte)Math.Clamp(Math.Round(old[j]+d[j]*scale),0,255);
                bool any=false;for(int j=0;j<3;j++)if(dst[k+j]!=src[k+j])any=true;
                if(any)changed[c]++;
                double dl=Math.Abs(L(dst[k+2],dst[k+1],dst[k])-L(r,g,b));sumLum+=dl;maxLum=Math.Max(maxLum,dl);
                // QA material mask: indexed color, never included in the delivered illustration.
                int[,] colors={{240,100,100},{150,80,220},{250,180,80},{60,180,220},{80,200,140},{240,100,200}};
                mask[k]=(byte)colors[c,2];mask[k+1]=(byte)colors[c,1];mask[k+2]=(byte)colors[c,0];
            }
            Save(image,dst,output);using(var diagnostic=new Bitmap(w,h,PixelFormat.Format32bppArgb))Save(diagnostic,mask,maskPath);
            var text=new StringBuilder("{\"width\":1536,\"height\":1024,\"meanLumaChange\":");
            text.Append(F(sumLum/n)).Append(",\"maxLumaChange\":").Append(F(maxLum)).Append(",\"unchangedPureWhitePixels\":").Append(unchangedBackground).Append(",\"materials\":[");
            string[] names={"skin","purple_ribbons","cat_inner","cat_white","tail_white","cutout_insets"};
            for(int c=0;c<6;c++) {if(c>0)text.Append(',');text.Append("{\"id\":\"").Append(names[c]).Append("\",\"sourceSamples\":").Append(sums[c,2]).Append(",\"referenceSamples\":").Append(sums[c,5]).Append(",\"chromaDeltaRB\":[").Append(F(delta[c,0])).Append(',').Append(F(delta[c,1])).Append("],\"transform\":\"").Append(c==1||c==5?"chroma_similarity":"chroma_offset").Append("\",\"similarityComplex\":[").Append(F(similarity[c,0])).Append(',').Append(F(similarity[c,1])).Append("],\"changedPixels\":").Append(changed[c]).Append('}');}
            return text.Append("]}").ToString();
        }
    }
    public static string BrightenWhites(string input,string reference,string output,string maskPath) {
        if(System.IO.File.Exists(output)||System.IO.File.Exists(maskPath))throw new InvalidOperationException("Output already exists.");
        using(var image=Load(input))using(var guide=Load(reference)) {
            int w=image.Width,h=image.Height,n=w*h;
            if(w!=1536||h!=1024||guide.Size!=image.Size)throw new InvalidOperationException("Unsupported layout.");
            byte[] src=Read(image),dst=(byte[])src.Clone(),refdata=Read(guide),mask=new byte[n*4];
            int[,] hair={{110,12,510,515},{640,12,940,515},{1040,12,1430,515}};
            int[,] dress={{130,267,493,799},{570,267,881,799},{1055,430,1411,799}};
            int[] changed=new int[2];double[,] sums=new double[2,4];double[] selection=new double[n];int[] region=new int[n];
            for(int p=0;p<n;p++) {
                int x=p%w,y=p/w,k=p*4;mask[k+3]=255;
                if(In(x,y,cat)||Tail(x,y))continue;
                bool isHair=In(x,y,hair),isDress=In(x,y,dress);
                if(!isHair&&!isDress)continue;
                double b=src[k],g=src[k+1],r=src[k+2],l=L(r,g,b);
                if(r==255&&g==255&&b==255)continue;
                double spread=Math.Max(r,Math.Max(g,b))-Math.Min(r,Math.Min(g,b));
                double weight=Smooth((l-135)/60)*Smooth((40-spread)/20)*(1-Smooth(Warm(r,g,b)/.4))*(1-Smooth(Purple(r,g,b)/.4));
                if(weight<=0)continue;
                selection[p]=weight;region[p]=isHair?0:1;
            }
            // Smooth ONLY the selection field to prevent color-threshold speckles; image is never blurred.
            for(int p=0;p<n;p++) {
                int x=p%w,y=p/w,k=p*4;double b=src[k],g=src[k+1],r=src[k+2],l=L(r,g,b);
                if(selection[p]<=0||Warm(r,g,b)>.4||Purple(r,g,b)>.4)continue;
                double weight=0,den=0;
                for(int dy=-4;dy<=4;dy++)for(int dx=-4;dx<=4;dx++) {
                    int xx=x+dx,yy=y+dy;if(xx<0||yy<0||xx>=w||yy>=h)continue;
                    double q=Math.Exp(-(dx*dx+dy*dy)/8.0);weight+=q*selection[yy*w+xx];den+=q;
                }
                weight/=den;int c=region[p];double strength=.32;
                // Continuous screen-to-white curve; no hue jumps or new illumination texture.
                double[] channels={b,g,r};
                for(int j=0;j<3;j++)dst[k+j]=(byte)Math.Clamp(Math.Round(channels[j]+(255-channels[j])*strength*weight),0,255);
                bool diff=false;for(int j=0;j<3;j++)if(dst[k+j]!=src[k+j])diff=true;
                if(diff) {
                    changed[c]++;sums[c,0]+=l;sums[c,1]+=L(dst[k+2],dst[k+1],dst[k]);
                    sums[c,2]+=L(refdata[k+2],refdata[k+1],refdata[k]);sums[c,3]++;
                }
                mask[k]=(byte)(c==0?230:80);mask[k+1]=(byte)(c==0?180:220);mask[k+2]=70;
            }
            Save(image,dst,output);using(var diagnostic=new Bitmap(w,h,PixelFormat.Format32bppArgb))Save(diagnostic,mask,maskPath);
            return "{\"method\":\"continuous_white_tone_curve\",\"hairChangedPixels\":"+changed[0]+",\"dressChangedPixels\":"+changed[1]+
                ",\"hairMeanBefore\":"+F(sums[0,0]/Math.Max(1,sums[0,3]))+",\"hairMeanAfter\":"+F(sums[0,1]/Math.Max(1,sums[0,3]))+
                ",\"dressMeanBefore\":"+F(sums[1,0]/Math.Max(1,sums[1,3]))+",\"dressMeanAfter\":"+F(sums[1,1]/Math.Max(1,sums[1,3]))+"}";
        }
    }
    public static string Verify(string input,string output,string maskPath) {
        using(var a=Load(input))using(var b=Load(output))using(var m=Load(maskPath)) {
            if(a.Size!=b.Size||a.Size!=m.Size)throw new InvalidOperationException("Dimensions changed.");
            byte[] x=Read(a),y=Read(b),mask=Read(m);int outside=0,alpha=0,whiteChanged=0,changed=0;
            for(int k=0;k<x.Length;k+=4) {
                bool diff=x[k]!=y[k]||x[k+1]!=y[k+1]||x[k+2]!=y[k+2];
                if(diff)changed++;
                if(diff&&mask[k]==0&&mask[k+1]==0&&mask[k+2]==0)outside++;
                if(x[k+3]!=y[k+3])alpha++;
                if(diff&&x[k]==255&&x[k+1]==255&&x[k+2]==255)whiteChanged++;
            }
            if(outside!=0||alpha!=0||whiteChanged!=0)throw new InvalidOperationException("Color-only scope check failed.");
            return "{\"outsideMaskChanges\":"+outside+",\"alphaChanges\":"+alpha+",\"pureWhiteChanges\":"+whiteChanged+",\"changedPixels\":"+changed+",\"dimensionsPreserved\":true}";
        }
    }
    static string F(double v) {return v.ToString("F6",System.Globalization.CultureInfo.InvariantCulture);}
    static void Save(Bitmap image,byte[] data,string path) {
        var bits=image.LockBits(new Rectangle(0,0,image.Width,image.Height),ImageLockMode.WriteOnly,PixelFormat.Format32bppArgb);
        Marshal.Copy(data,0,bits.Scan0,data.Length);image.UnlockBits(bits);image.Save(path,ImageFormat.Png);
    }
}
