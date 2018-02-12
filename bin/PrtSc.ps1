[Reflection.Assembly]::LoadWithPartialName("System.Drawing");
[Reflection.Assembly]::LoadWithPartialName("System.Web");
[Reflection.Assembly]::LoadWithPartialName("System.Drawing");
[Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms");

function prtsc(){
    $path=(get-date -UFormat "%s.png");
    foreach ($screen in [System.Windows.Forms.Screen]::AllScreens){$x=$screen.Bounds.Width;$y=$screen.Bounds.Height;}
    $bounds = [Drawing.Rectangle]::FromLTRB(0, 0, $x, $y);
    $bmp = New-Object Drawing.Bitmap $x, $y;
    $graphics = [Drawing.Graphics]::FromImage($bmp);
    $graphics.CopyFromScreen($bounds.Location, [Drawing.Point]::Empty, $bounds.size);
    $bmp.Save($path);$graphics.Dispose();$bmp.Dispose();
    "$path";
}
prtsc
