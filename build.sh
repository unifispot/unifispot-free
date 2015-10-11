BUILDDIR=build
PKGDIR=build/unifispot

if [ -d "$BUILDDIR" ]; then
    printf '%s\n' "Removing Build DIrectory ($DIR)"
    rm -rf "$BUILDDIR"
fi
mkdir "$BUILDDIR"
mkdir "$PKGDIR"

cp -r bluespot/ "$PKGDIR/"
cp -r config/ "$PKGDIR/"
cp -r env/ "$PKGDIR/"
cp example.yaml "$PKGDIR/"
cp manage.py "$PKGDIR/"
cp unifispot.conf "$PKGDIR/"
cp unifispot.wsgi "$PKGDIR/"

echo "-----------------------------Compiling py files into pyc-------------------"
python -m compileall build/unifispot/
echo "-----------------------------Deleting py files-------------------"
find ./build/unifispot/bluespot -name "*.py" -type f -exec rm {} \;
find ./build/unifispot/config -name "*.py" -type f -exec rm {} \;
rm ./build/unifispot/manage.py

echo "-----------------------------Building Packages-----------------------------"
cd build 
fpm -s dir -t deb -n unifispot -v 0.1 -d "python,python-dev,apache2,libapache2-mod-wsgi"  --after-install ../post_install.sh -a i686 unifispot/=/var/www/unifispot 
fpm -s dir -t deb -n unifispot -v 0.1 -d "python,python-dev,apache2,libapache2-mod-wsgi"  --after-install ../post_install.sh  unifispot/=/var/www/unifispot 
tar -zcvf unifispot.tar.gz unifispot
