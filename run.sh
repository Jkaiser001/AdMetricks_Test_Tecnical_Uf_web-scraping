#!/usr/bin/bash

docker build . -t app_uf_web_scraping
docker run -d -p 8080:8000 -v $(pwd)/logs:/app/log --name app_uf_web_scraping app_uf_web_scraping:latest