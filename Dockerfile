# use the official kics image as basis image
FROM checkmarx/kics:v1.7.11-debian

WORKDIR /

ENV GITLAB_ACCESS_TOKEN=GITLAB_ACCESS_TOKEN

# install necessary packages
RUN set -eux; \
  apt-get update && \
  apt-get install -y --no-install-recommends \
  python3=3.7.3-1 \
  python3-pip=18.1-5 \
  python3-setuptools=40.8.0-1 && \
  apt-get clean all && \
  rm -rf /var/lib/apt/lists/*

# install python packages from our requirements.txt
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# copy and execute repo_scanner.py
COPY repo_scanner.py .
COPY templates ./templates/.
ENTRYPOINT ["python3", "repo_scanner.py"]
