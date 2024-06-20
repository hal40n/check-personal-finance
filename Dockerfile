FROM python:latest

WORKDIR /app

RUN apt-get update \
    && apt-get install -y \
    git \
    zip \
    unzip \
    vim \
    libfreetype6-dev \
    libjpeg62-turbo-dev \
    libmcrypt-dev \
    libpng-dev \
    libfontconfig1 \
    libxrender1 \
    libzip-dev \
    netcat-openbsd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV NVM_DIR=/root/.nvm
ENV NODE_VERSION=18.17.0

RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash \
    && . "$NVM_DIR/nvm.sh" \
    && nvm install ${NODE_VERSION} \
    && nvm use ${NODE_VERSION} \
    && nvm alias default ${NODE_VERSION} \
    && ln -s "$NVM_DIR/versions/node/$(nvm current)/bin/node" /usr/bin/node \
    && ln -s "$NVM_DIR/versions/node/$(nvm current)/bin/npm" /usr/bin/npm \
    && node --version \
    && npm --version

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

COPY package*.json ./

RUN npm install

COPY . .

COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

CMD ["/wait-for-it.sh", "db:3306", "--", "python", "app.py"]
