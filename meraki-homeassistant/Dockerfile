# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM

LABEL \
  io.hass.version="VERSION" \
  io.hass.type="addon" \
  io.hass.arch="armhf|aarch64|i386|amd64"

ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN apk add py3-pip py3-setuptools

RUN apk add py3-requests
RUN pip install meraki --break-system-packages

WORKDIR /data

# Copy data for add-on
COPY run.sh /run.sh
copy merakisync.py /merakisync.py

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]