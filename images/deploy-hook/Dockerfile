FROM ubuntu:17.04

RUN apt-get update --yes
RUN apt-get install --yes \
      python3 \
      python3-pip \
      git \
      curl \
      git-crypt

# Install helm!
RUN curl -ssL https://storage.googleapis.com/kubernetes-helm/helm-v2.5.1-linux-amd64.tar.gz | tar -xz -C /usr/local/bin --strip-components 1 linux-amd64/helm

RUN chmod +x /usr/local/bin/helm

RUN pip3 install --no-cache-dir tornado

COPY app.py /srv/app.py

EXPOSE 8888
CMD python3 /srv/app.py
