# My step-by-step

This was done in a fresh install of Ubuntu Desktop 15.10.

### Install NodeJS (based on [this](https://github.com/nodejs/node-v0.x-archive/wiki/Installing-Node.js-via-package-manager))
* curl -sL https://deb.nodesource.com/setup_5.x | sudo -E bash -
* sudo apt-get install --yes nodejs

### Install docker (based on [this](https://docs.docker.com/engine/installation/ubuntulinux/))
* sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
* Open /etc/apt/sources.list.d/docker.list in your favourite editor, eg:
	* sudo vim /etc/apt/sources.list.d/docker.list
* Add the line (for Ubuntu 15.04):
	* deb https://apt.dockerproject.org/repo ubuntu-vivid main
* **OR** Add the line (for Ubuntu 15.10):
	* deb https://apt.dockerproject.org/repo ubuntu-wily main
* Save and close the file
* sudo apt-get update
* sudo apt-get purge lxc-docker
* sudo apt-get install linux-image-extra-$(uname -r)
* sudo apt-get install docker-engine
* sudo service docker start

### Install docker-compose (based on [this](https://docs.docker.com/compose/install/))
* sudo su -
* curl -L https://github.com/docker/compose/releases/download/1.5.2/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
* chmod +x /usr/local/bin/docker-compose
* curl -L https://raw.githubusercontent.com/docker/compose/$(docker-compose --version | awk 'NR==1{print $NF}')/contrib/completion/bash/docker-compose > /etc/bash_completion.d/docker-compose
* exit

### Install ruby and sass
* sudo apt-get install ruby
* sudo gem install sass

### Get the source code (use your forked project, if any).

* git clone -b development https://github.com/unicef/rhizome.git
* bump the version of the node-sass package to 3.4.2 in the <rhizome-repository>/webapp/package.json file
* rename the file <rhizome-repository>/webapp/src/component/CsvMenuItem.jsx to <rhizome-repository>/webapp/src/component/CSVMenuItem.jsx

### Start the dockelets
* got to <rhizome-repository>
* sudo docker-compose build
* sudo docker-compose up

### Developing
* go to <rhizome-repository>/webapp
* sudo npm install -g gulp
* sudo npm install -g node-gyp
* npm install
* gulp dev
