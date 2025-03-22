FROM nginx:1.27.1-bookworm
LABEL authors="VovkaGoodwin"

RUN rm /etc/nginx/conf.d/default.conf
COPY ./dockerization/nginx/nginx.conf /etc/nginx/nginx.conf

RUN mkdir  /etc/nginx/sites-available
RUN mkdir  /etc/nginx/sites-enabled

COPY ./dockerization/nginx/sites-available/toyan-bot.conf /etc/nginx/sites-available/toyan-bot.conf
RUN ln -s /etc/nginx/sites-available/toyan-bot.conf /etc/nginx/sites-enabled/