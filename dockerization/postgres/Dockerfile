FROM postgres:17.2-bullseye

# === Устанавливаем пакет locales ===
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y locales

# === Раскоменчиваем нужную локаль и устанавливаем ее ===
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8

# === Задаем значения переменным ===
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

EXPOSE 5432