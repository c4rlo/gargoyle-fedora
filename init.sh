url=http://garglk.googlecode.com/files/gargoyle-2011.1-sources.zip
zipname=gargoyle-2011.1-sources.zip
dirname=src

if [[ -f $zipname ]]; then
    echo "$zipname already exists in current dir, using it"
elif [[ $# -gt 0 ]]; then
    cp $1 $zipname
else
    curl -o $zipname $url || exit 1
fi

rm -rf $dirname
unzip -q -d $dirname $zipname
rm $zipname
cd $dirname
rm -rf terps/hugo licenses/HUGO* \
       fonts/LuxiMono* garglk/lm?.hex garglk/LuxiMono.txt licenses/LUXI*
cd support
rm -rf dylibs freetype iplinux libjpeg libpng sdl sdl_sound zlib
