FROM python:3.11.4-slim
ENV PATH=$PATH:/opt
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        procps=2:4.0.2-3 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean
COPY requirements.txt /
RUN pip install --no-cache-dir -r requirements.txt \
    && rm requirements.txt
COPY local_app_prepper.py /opt/
COPY templates /opt/templates
COPY prepper /opt/prepper
