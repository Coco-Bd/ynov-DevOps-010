FROM quay.io/ansible/awx-ee:latest

USER root

RUN microdnf install -y docker-cli && \
    microdnf clean all

COPY requirements.yml /tmp/requirements.yml
RUN ansible-galaxy collection install -r /tmp/requirements.yml

USER 1000