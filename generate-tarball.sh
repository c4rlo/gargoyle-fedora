#!/bin/bash

# The upstream sources contain pieces of source code whose licenses are not
# allowed in Fedora -- we cannot ship it even in the SRPM.
# Use this script to download the upstream sources and remove the problematic
# files, resulting in the compressed tar file that we use as a starting point
# for our RPM.

version=2011.1

name=gargoyle-$version
url=http://garglk.googlecode.com/files/$name-sources.zip
zipname=$name-sources.zip
tarname=$name.tar.bz2

if [[ -e $name ]]; then
    echo "$name must not exist in the current directory"
    exit 1
elif [[ -e $tarname ]]; then
    echo "$tarname must not exist in the current directory"
    exit 1
fi

if [[ -f $zipname ]]; then
    echo "$zipname already exists in current directory, using it"
elif [[ $# -gt 0 ]]; then
    cp $1 $zipname
elif which curl >/dev/null; [[ $? != 0 ]]; then
    echo "'curl' must be installed to download sources"
    exit 2
else
    echo "Downloading sources from $url"
    curl -o $zipname $url
fi

echo "Unzipping"
unzip -q -d $name $zipname
rm $zipname

echo "Removing unneeded files"
cd $name
rm -rf terps/hugo licenses/HUGO* \
       fonts/LuxiMono* garglk/lm?.hex garglk/LuxiMono.txt licenses/LUXI* \
       support
cd ..

echo "Compressing"
tar -cjf $tarname $name
rm -rf $name
