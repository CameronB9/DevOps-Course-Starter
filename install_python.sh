sudo yum update -y
sudo yum groupinstall "Development Tools" -y
# If installing a version of Python < 3.10, then use openssl-devel in place of openssl11-devel
sudo yum install libffi-devel bzip2-devel wget openssl11-devel -y

wget https://www.python.org/ftp/python/3.10.2/Python-3.10.2.tgz
tar -xf Python-3.10.2.tgz
cd Python-3.10.2/

sudo ./configure --enable-optimizations
sudo make -j $(nproc)
sudo make install # or "sudo make install" to override existing Python