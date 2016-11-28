# LAMP STACK

We use a docker container using simple ubuntu base, installing MYSQL, apache2 and php5 on it afterward.
I added 2 shared volume /home/apache to /usr/local/apache2/htdocs and /home/apache/www to /var/www

`sudo docker run --name georgesLAMP -p 80:80 -p 443:443 -p 3306:3306 -itd -v /home/apache:/usr/local/apache2/htdocs -v /home/apache/www:/var/www ubuntu:latest`