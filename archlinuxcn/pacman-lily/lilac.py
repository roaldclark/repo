from types import SimpleNamespace

from lilaclib import *

g = SimpleNamespace()

def pre_build():
  g.files = download_official_pkgbuild('pacman')

  package = False
  for line in edit_file('PKGBUILD'):
    if line.startswith('pkgname='):
      line = 'pkgname=pacman-lily'
    elif line.startswith('pkgdesc='):
      line = line[:-1] + ' (no disabling-server-on-error)"'
    elif line.startswith('provides=('):
      line = line.replace(')', ' "pacman=$pkgver")\n') + "conflicts=('pacman')"
    elif line.startswith('groups=('):
      continue
    elif line.startswith('source=('):
      line = 'install=lily.install\n' + line.replace('(', '(pacman.patch\n        pacman-syncdb\n        ')
    elif line.startswith('sha256sums=('):
      line = line.replace('(', '(38cffbcb9d912111549fdf3cf151d6e2af4a35a9af0c347f209b7bea9f1dc09e\n            207d5cee261bba18e650bbd2c249ffd8fe9c1dbd7de6b241d8bf011848faa70b\n            ')
    elif line.startswith('package() '):
      package = True
    elif package and line.startswith('}'):
      line = '  install -m755 "$srcdir/pacman-syncdb" "$pkgdir/usr/bin"\n' + line
      package = False

    if '$pkgname' in line:
      line = line.replace('$pkgname', 'pacman')
    if '${pkgname}' in line:
      line = line.replace('${pkgname}', 'pacman')
    print(line)

def post_build():
  git_add_files(g.files)
  git_commit()
