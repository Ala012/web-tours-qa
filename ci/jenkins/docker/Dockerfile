# Jenkins + Python + Google Chrome pour le mini-projet QA WebTours.
#
# Le conteneur execute les tests Selenium/pytest. WebTours reste sur l'hote
# Windows et est joignable via host.docker.internal:1080.
FROM jenkins/jenkins:lts-jdk21

USER root

ENV DEBIAN_FRONTEND=noninteractive

# Python (tests) + curl (verification WebTours) + Google Chrome (Selenium).
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates curl gnupg wget \
        python3 python3-venv python3-pip \
    && wget -q -O /tmp/google-chrome.deb \
        https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y /tmp/google-chrome.deb \
    && rm -f /tmp/google-chrome.deb \
    && rm -rf /var/lib/apt/lists/*

# Environnement Python dedie, accessible en ecriture par l'utilisateur jenkins.
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip \
    && chown -R jenkins:jenkins /opt/venv

ENV PATH="/opt/venv/bin:${PATH}" \
    PYTHONUTF8=1 \
    PYTHONUNBUFFERED=1

# Dependances installees a la construction (deja presentes au premier build).
COPY automation/requirements.txt /tmp/requirements.txt
RUN /opt/venv/bin/pip install -r /tmp/requirements.txt \
    && rm -f /tmp/requirements.txt

# Plugins Jenkins necessaires au pipeline.
COPY ci/jenkins/docker/plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/ref/plugins.txt

USER jenkins
