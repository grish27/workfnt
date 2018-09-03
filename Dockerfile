FROM jenkins:2.60.3
MAINTAINER GrigorJ

#get rid of admin password setup
ENV JAVA_OPTS="-Djenkins.install.runSetupWizard=false"
 
#automatically installing all plugins
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN /usr/local/bin/install-plugins.sh < /usr/share/jenkins/ref/plugins.txt

#adding scripts
COPY groovy/* /usr/share/jenkins/ref/init.groovy.d/

#install Filebeat
USER root
 
RUN curl -o /tmp/filebeat_1.0.1_amd64.deb https://download.elastic.co/beats/filebeat/filebeat_1.0.1_amd64.deb && \
   dpkg -i /tmp/filebeat_1.0.1_amd64.deb &&  apt-get install
 
COPY filebeat.yml /etc/filebeat/filebeat.yml

COPY ["entrypoint.sh", "/"]
 
RUN chmod +x /entrypoint.sh
 
ENTRYPOINT ["/bin/bash","-c","./entrypoint.sh"]