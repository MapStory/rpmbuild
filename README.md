MapStory rpmbuild for Enterprise Linux 6
----------------------

__Using Vagrant - https://www.vagrantup.com/__

```bash
git clone https://github.com/MapStory/rpmbuild.git
cd rpmbuild
vagrant up
vagrant ssh
QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild --define '_topdir /vagrant' -bb /vagrant/SPECS/mapstory.spec
vagrant destroy
```