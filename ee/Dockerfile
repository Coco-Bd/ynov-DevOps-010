FROM quay.io/ansible/awx-ee:latest

USER root

COPY requirements.yml /tmp/requirements.yml
RUN ansible-galaxy collection install -r /tmp/requirements.yml -p /usr/share/ansible/collections

RUN python3 -m ensurepip && \
    python3 -m pip install --no-cache-dir docker

USER 1000