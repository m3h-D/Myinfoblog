FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
# ADD conf.d/ /etc/nginx/conf.d
# COPY src/nginx/django_tickets.conf /etc/nginx/conf.d
COPY ./django_tickets.conf /etc/nginx/conf.d
