[CmdletBinding()]
param(
    [string]$SourcePath = 'D:/desktop-pet/assets/characters/base-templates/base-b-archer/v04/base-b-archer-five-fingers-blue-purple-eyes-front-v04.png',
    [string]$OutputPath = 'D:/desktop-pet/assets/characters/base-templates/base-b-archer/v06/base-b-archer-continuous-head-skin-front-v06.png',
    [string]$MaskPath = 'D:/desktop-pet/assets/characters/base-templates/base-b-archer/v06/head-skin-edit-mask.png'
)

$ErrorActionPreference = 'Stop'
if ((Test-Path -LiteralPath $OutputPath) -or (Test-Path -LiteralPath $MaskPath)) {
    throw 'Refusing to overwrite an existing image or mask.'
}
Add-Type -AssemblyName System.Drawing
Add-Type -ReferencedAssemblies System.Drawing -TypeDefinition @'
using System;
using System.Drawing;
using System.Drawing.Imaging;

public static class ArcherHeadColorV06 {
    static double Smooth(double t) { t=Math.Max(0,Math.Min(1,t)); return t*t*(3-2*t); }
    static double OutsideEllipse(int x,int y,double cx,double cy,double rx,double ry) {
        double dx=(x-cx)/rx,dy=(y-cy)/ry;
        return Smooth((Math.Sqrt(dx*dx+dy*dy)-1.0)*Math.Min(rx,ry)/3.0);
    }
    static int Blend(int oldValue,double value,int alpha) {
        return Math.Max(0,Math.Min(255,(int)Math.Round((oldValue*(255-alpha)+value*alpha)/255.0)));
    }
    public static int Run(string sourcePath,string outputPath,string maskPath) {
        using (var source=new Bitmap(sourcePath))
        using (var output=source.Clone(new Rectangle(0,0,source.Width,source.Height),PixelFormat.Format32bppArgb))
        using (var mask=new Bitmap(source.Width,source.Height,PixelFormat.Format24bppRgb)) {
            if(source.Width!=1024 || source.Height!=1536) throw new Exception("Unexpected source canvas");
            using(var g=Graphics.FromImage(mask)) g.Clear(Color.Black);
            int edited=0;
            // All operations are confined to the original head. Row bounds come from its existing contour.
            for(int y=175;y<=353;y++) {
                int left=9999,right=-1;
                for(int x=438;x<=586;x++) {
                    Color c=source.GetPixel(x,y);
                    if(Math.Min(c.R,Math.Min(c.G,c.B))<225) { left=Math.Min(left,x);right=Math.Max(right,x); }
                }
                if(right-left<6) continue;
                for(int x=left+1;x<right;x++) {
                    Color c=source.GetPixel(x,y);
                    double edge=Math.Min(x-left-1,right-x-1);
                    double w=Smooth(edge/4.0)*Smooth((y-175)/5.0)*Smooth((353-y)/5.0);
                    // Protect colored linework and smoothly blend anti-aliased skin boundaries.
                    w*=Smooth((Math.Min(c.R,Math.Min(c.G,c.B))-195)/37.0);
                    // Preserve irises, lashes, eyebrows, nose and mouth with feathered exclusions.
                    w*=OutsideEllipse(x,y,477,286,27,22);
                    w*=OutsideEllipse(x,y,545,286,27,22);
                    w*=OutsideEllipse(x,y,478,251,21,8);
                    w*=OutsideEllipse(x,y,546,251,21,8);
                    w*=OutsideEllipse(x,y,511,314,5,4);
                    w*=OutsideEllipse(x,y,511,326,10,5);
                    int alpha=(int)Math.Round(255*w);
                    if(alpha==0) continue;
                    double side=Math.Pow((x-512)/75.0,2);
                    double lower=Smooth((y-260)/93.0);
                    double blush=Math.Exp(-Math.Pow((x-465)/16.0,2)-Math.Pow((y-313)/12.0,2))
                               +Math.Exp(-Math.Pow((x-559)/16.0,2)-Math.Pow((y-313)/12.0,2));
                    // A continuous pale pink-ivory field, with broad restrained frontal shading.
                    double r=254.4;
                    double g=241.3-1.0*side-0.6*lower-3.4*blush;
                    double b=238.7-1.2*side-0.5*lower-2.5*blush;
                    output.SetPixel(x,y,Color.FromArgb(c.A,Blend(c.R,r,alpha),Blend(c.G,g,alpha),Blend(c.B,b,alpha)));
                    mask.SetPixel(x,y,Color.FromArgb(alpha,alpha,alpha));
                    edited++;
                }
            }
            output.Save(outputPath,ImageFormat.Png);
            mask.Save(maskPath,ImageFormat.Png);
            return edited;
        }
    }
}
'@

$outputFolder = Split-Path -Parent $OutputPath
$maskFolder = Split-Path -Parent $MaskPath
New-Item -ItemType Directory -Path $outputFolder -Force | Out-Null
New-Item -ItemType Directory -Path $maskFolder -Force | Out-Null
$pixelCount = [ArcherHeadColorV06]::Run($SourcePath, $OutputPath, $MaskPath)
[pscustomobject]@{ Output = $OutputPath; Mask = $MaskPath; MaskedPixels = $pixelCount } | ConvertTo-Json
