Exec { path => '/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin' }

# Global variables
$inc_file_path = '/vagrant/manifests/files' # Absolute path to the files directory (If you're using vagrant, you can leave it alone.)
$tz = 'Europe/Stockholm' # Timezone
$user = 'user1' # User to create
$password = 'password1' # The user's password
$project = 'bidpart' # Used in nginx and uwsgi
$domain_name = 'bidpart.se' # Used in nginx, uwsgi and virtualenv directory
$db_name = 'bidpart_django' # Mysql database name to create
$db_user = 'user1' # Mysql username to create
$db_password = 'password1' # Mysql password for $db_user

include timezone
include apt
include mysql
include python
include pildeps
include software
include nodejs

class timezone {
  package { "tzdata":
    ensure => latest,
    require => Class['apt']
  }

  file { "/etc/localtime":
    require => Package["tzdata"],
    source => "file:///usr/share/zoneinfo/${tz}",
  }
}


class apt {
  exec { 'apt-get update':
    timeout => 0
  }

  package { 'python-software-properties':
    ensure => latest,
    require => Exec['apt-get update']
  }

  exec { 'add-apt-repository ppa:nginx/stable':
    require => Package['python-software-properties'],
    before => Exec['last ppa']
  }

  exec { 'last ppa':
    command => 'add-apt-repository ppa:git-core/ppa',
    require => Package['python-software-properties']
  }

  exec { 'apt-get update again':
    command => 'apt-get update',
    timeout => 0,
    require => Exec['last ppa']
  }
}


class mysql {

  package { 'mysql-server':
    ensure => latest,
    require => Class['apt']
  }

  package { 'libmysqlclient-dev':
    ensure => latest,
    require => Class['apt']
  }

  service { 'mysql':
    ensure => running,
    enable => true,
    require => Package['mysql-server']
  }

  exec { 'grant user db':
    command => 'mysql -u root -e "CREATE DATABASE IF NOT EXISTS bidpart_django CHARACTER SET utf8;"',
    require => Service['mysql']
  }
}

class python {
  package { 'curl':
    ensure => latest,
    require => Class['apt']
  }

  package { 'python':
    ensure => latest,
    require => Class['apt']
  }

  package { 'python-dev':
    ensure => latest,
    require => Class['apt']
  }

  exec { 'install-distribute':
    command => 'curl http://python-distribute.org/distribute_setup.py | python',
    require => Package['python', 'curl']
  }

  exec { 'install-pip':
    command => 'curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python',
    require => Exec['install-distribute']
  }
}


class pildeps {
  package { ['python-imaging', 'libjpeg-dev', 'libfreetype6-dev']:
    ensure => latest,
    require => Class['apt'],
    before => Exec['pil png', 'pil jpg', 'pil freetype']
  }

  exec { 'pil png':
    command => 'sudo ln -s /usr/lib/`uname -i`-linux-gnu/libz.so /usr/lib/',
    unless => 'test -L /usr/lib/libz.so'
  }

  exec { 'pil jpg':
    command => 'sudo ln -s /usr/lib/`uname -i`-linux-gnu/libjpeg.so /usr/lib/',
    unless => 'test -L /usr/lib/libjpeg.so'
  }

  exec { 'pil freetype':
    command => 'sudo ln -s /usr/lib/`uname -i`-linux-gnu/libfreetype.so /usr/lib/',
    unless => 'test -L /usr/lib/libfreetype.so'
  }
}

class nodejs($node_ver = 'v0.8.22') {
  $node_tar = "node-$node_ver.tar.gz"
  $node_unpacked = "node-$node_ver"

  package { "build-essential":
    ensure => latest
  }

  exec { 'download_node':
    command     => "curl -o $node_tar http://nodejs.org/dist/${node_ver}/${node_tar}",
    cwd         => '/tmp',
    path        => ['/usr/bin/', '/bin/'],
    creates     => "/tmp/${node_tar}",
    require     => Package["curl"],
    unless      => "which node && test `node -v` = ${node_ver}"
  }

  exec { 'extract_node':
    command     => "tar -oxzf $node_tar",
    cwd         => '/tmp',
    require     => Exec['download_node'],
    creates     => "/tmp/${node_unpacked}",
    path        => ['/usr/bin/', '/bin/']
  }

  exec { 'configure_node':
    command     => "/bin/sh -c './configure'",
    cwd         => "/tmp/${node_unpacked}",
    require     => [ Exec["extract_node"], Package["build-essential"]],
    timeout     => 0,
    path        => ['/usr/bin/', '/bin/'],
  }

  exec { 'make_node':
    command     => 'make',
    cwd         => "/tmp/${node_unpacked}",
    require     => Exec['configure_node'],
    timeout     => 0,
    path        => ['/usr/bin/', '/bin/']
  }

  exec { 'install_node':
    command     => 'make install',
    cwd         => "/tmp/${node_unpacked}",
    require     => Exec['make_node'],
    timeout     => 0,
    path        => ['/usr/bin/', '/bin/'],
    unless      => "which node && test `node -v` = ${node_ver}"
  }
}

class software {
  package { 'git':
    ensure => latest,
    require => Class['apt']
  }

  package { 'node':
    ensure => latest,
    require => Class['apt']
  }

  package { 'npm':
    ensure => latest,
    require =>  [Class['nodejs'], Class['apt']]
  }

  exec { 'install-lessc':
    command => 'npm install less -g',
    require => [Class['nodejs'], Package['npm']]
  }



  exec { 'download_wkhtmltopdf':
    command     => "curl -o wkhtmltopdf.tar.bz2 https://wkhtmltopdf.googlecode.com/files/wkhtmltopdf-0.11.0_rc1-static-i386.tar.bz2",
    cwd         => '/tmp',
    path        => ['/usr/bin/', '/bin/'],
    creates     => "/tmp/wkhtmltopdf.tar.bz2",
    require     => Package["curl"]
  }
  exec { 'extract_wkhtmltopdf':
    command     => "tar -oxzf wkhtmltopdf.tar.bz2",
    cwd         => '/tmp',
    require     => Exec['download_wkhtmltopdf'],
    creates     => "/tmp/wkhtmltopdf",
    path        => ['/usr/bin/', '/bin/']
  }
  exec { 'move_wkhtmltopdf':
    command     => "mv wkhtmltopdf-i386 /usr/bin/wkhtmltopdf",
    cwd         => '/tmp/wkhtmltopdf',
    require     => Exec['extract_wkhtmltopdf'],
    creates     => "/usr/bin/wkhtmltopdf",
    path        => ['/usr/bin/', '/bin/']
  }
  exec { 'chmod_wkhtmltopdf':
    command     => "chmod a+x wkhtmltopdf",
    cwd         => '/usr/bin',
    require     => Exec['extract_wkhtmltopdf'],
    creates     => "/usr/bin/wkhtmltopdf",
    path        => ['/usr/bin/', '/bin/']
  }
}


