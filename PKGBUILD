# Maintainer: Matthew Wardrop <mister.wardrop@gmail.com>
pkgname=python2-mplstyles
pkgver=0.1
pkgrel=1
pkgdesc="A style collection for matplotlib."
arch=('i686' 'x86_64')
url=""
license=('GPL')
groups=()
depends=('python2' 'python2-matplotlib')
makedepends=()
provides=()
conflicts=()
replaces=()
backup=()
options=(!emptydirs)
install=
source=()
md5sums=()

package() {
  cd ".."
  #cd "$srcdir/$pkgname-$pkgver"
  python2 setup.py install --root="$pkgdir/" --optimize=1
}

# vim:set ts=2 sw=2 et:
