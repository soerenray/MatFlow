FROM node:17
WORKDIR /usr/src/app
COPY ./src ./src
COPY ./public ./public
COPY ./package*.json ./
COPY ./tsconfig.json ./
COPY ./vue.config.js ./
COPY ./babel.config.js ./
RUN npm install
CMD npm run serve -- --port 8081
# CMD bash
