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
# Home Assistant required tools
RUN apk add python3-dev py3-virtualenv autoconf alpine-sdk libressl-dev libxml2-dev libxslt-dev jpeg-dev libffi-dev libgudev-dev zlib-dev pkgconfig ffmpeg-libavformat ffmpeg-libavcodec ffmpeg-libavdevice ffmpeg-libavutil ffmpeg-libswscale ffmpeg-libswresample ffmpeg-libavfilter ffmpeg gammu-dev

RUN apk add py3-requests
# RUN python -m script.scaffold integration
RUN pip install meraki --break-system-packages

WORKDIR /data

# Copy data for add-on
COPY run.sh /run.sh
copy merakisync.py /merakisync.py

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]