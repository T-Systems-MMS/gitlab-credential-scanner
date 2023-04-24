# use the official kics image as basis image
FROM checkmarx/kics:v1.6.13-debian

ENV GITLAB_ACCESS_TOKEN=GITLAB_ACCESS_TOKEN

# install necessary packages
RUN set -eux; \
  apt-get update && \
  apt-get install -y --no-install-recommends \
  python3=3.10.6 \
  python3-pip=22.0.2 && \
  apt-get clean all && \
  rm -rf /var/lib/apt/lists/*

# install python packages from our requirements.txt
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# copy and execute repo_scanner.py
COPY repo_scanner.py .
COPY templates ./templates/.
ENTRYPOINT ["python3", "repo_scanner.py"]
