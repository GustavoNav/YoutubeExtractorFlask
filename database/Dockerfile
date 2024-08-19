FROM mysql:9.0

ENV MYSQL_ROOT_PASSWORD=adm321
ENV MYSQL_DATABASE=youtube_extractor_db
ENV MYSQL_USER=adm
ENV MYSQL_PASSWORD=adm321

COPY ./db.sql /docker-entrypoint-initdb.d/

EXPOSE 3306

CMD ["mysqld"]