# pull the official base image
FROM node:alpine
# set working direction
WORKDIR /SPA
# add `/app/node_modules/.bin` to $PATH
ENV PATH /SPA/node_modules/.bin:$PATH
# install application dependencies
COPY ./mu-app/package.json ./
COPY ./mu-app/package-lock.json ./
RUN npm i
RUN mkdir node_modules/.cache && chmod -R 777 node_modules/.cache

# add app
COPY ./mu-app/ ./
# start app
CMD ["npm", "start"]



# docker run \
# -it \
# --rm \
# -v ${PWD}/mu-app:/app \
# -v /app/node_modules \
# -p 3000:3000 \
# -e CHOKIDAR_USEPOLLING=true \
# mu-app