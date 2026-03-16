ARG BUILD_FROM
FROM $BUILD_FROM

# Install Python and required packages
RUN apk add --no-cache \
    python3 \
    py3-pip \
    jq \
    bash

# Install Python dependencies
RUN pip3 install --no-cache-dir requests

# Copy application files
COPY run.sh /run.sh
COPY tinderbot.py /tinderbot.py

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
