FROM php:8.2-apache

# 必要な拡張機能をインストール
RUN apt-get update && apt-get install -y \
    libfreetype6-dev \
    libjpeg62-turbo-dev \
    libpng-dev \
    git \
    zip \
    unzip \
    vim \
    libpng-dev \
    libpq-dev \
    libonig-dev \
    libxml2-dev \
    libzip-dev \
    wget \
    msmtp \
    msmtp-mta \
    libcurl4-openssl-dev \
    && docker-php-ext-install curl pdo pdo_mysql mysqli \
    && rm -rf /var/lib/apt/lists/*

# Composerをインストール
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Apacheの設定
RUN chown -R www-data:www-data /var/www/html
RUN a2enmod rewrite