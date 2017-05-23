#/bin/bash

echo Start installation
yum -y update
yum -y install git vim net-tools openssh-server openssh-clients wget pciutils screen
yum -y group install "Development Tools"

chkconfig sshd on
service sshd start

## DOCKER ##
tee /etc/yum.repos.d/docker.repo <<-'EOF'
[dockerrepo]
name=Docker Repository
baseurl=https://yum.dockerproject.org/repo/main/centos/7/
enabled=1
gpgcheck=1
gpgkey=https://yum.dockerproject.org/gpg
EOF

yum -y install docker-engine-1.12.5-1.el7

wget -P /root/tmp https://github.com/NVIDIA/nvidia-docker/releases/download/v1.0.0-rc.3/nvidia-docker-1.0.0.rc.3-1.x86_64.rpm
rpm -i /root/tmp/nvidia-docker*.rpm && rm /root/tmp/nvidia-docker*.rpm

systemctl enable docker.service
systemctl start docker
chkconfig docker on

systemctl enable nvidia-docker.service
systemctl start nvidia-docker
chkconfig nvidia-docker on


# GPU

mkdir -p /root/tmp
cd /root/tmp
rm -f NVIDIA-Linux-*
#wget -q http://us.download.nvidia.com/XFree86/Linux-x86_64/340.98/NVIDIA-Linux-x86_64-340.98.run
wget -q http://us.download.nvidia.com/XFree86/Linux-x86_64/367.44/NVIDIA-Linux-x86_64-367.44.run
chmod +x `ls NVIDIA-Linux-*.run`

echo 'blacklist nouveau' > /etc/modprobe.d/nouveau.conf 
echo 'options nouveau modeset=0' >> /etc/modprobe.d/nouveau.conf
mv /boot/initramfs-$(uname -r).img /boot/initramfs-$(uname -r).img.bak
dracut -v /boot/initramfs-$(uname -r).img $(uname -r)

# reboot

## AFTER REBOOT ##
#sh `ls NVIDIA-Linux-*.run` -q -a -n -X -s

