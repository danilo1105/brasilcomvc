FROM ubuntu:14.04

RUN apt-get update -q && apt-get upgrade -yq
RUN apt-get install -yq --fix-missing binutils build-essential git gettext gdal-bin libgeoip1 libproj-dev libpq-dev npm python-dev python-pip wget && apt-get clean
RUN ln -s /usr/bin/nodejs /usr/bin/node

RUN wget https://bin.equinox.io/c/ekMN3bCZFUn/forego-stable-linux-amd64.tgz
RUN tar xvf forego-stable-linux-amd64.tgz -C /usr/local/bin && chmod +x /usr/local/bin/forego

ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
ADD package.json /app/package.json
ADD bower.json /app/bower.json

ADD . /app
WORKDIR /app

USER nobody

# RUN python manage.py makemigrations && python manage.py migrate
RUN npm install

EXPOSE 8000

ENTRYPOINT ["/usr/local/bin/forego"]
CMD ["start", "-p", "8000", "web"]

