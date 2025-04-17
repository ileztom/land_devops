FROM nginx

COPY . /usr/share/nginx/html/assets
COPY . /usr/share/nginx/html/image
COPY . /usr/share/nginx/html/css
COPY . /usr/share/nginx/html
