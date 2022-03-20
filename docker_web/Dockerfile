FROM node:17
WORKDIR /usr/src/app
COPY ./matflow/frontend/src ./matflow/frontend/src
COPY ./matflow/frontend/public ./matflow/frontend/public
COPY ./package*.json ./
COPY ./tsconfig.json ./
COPY ./vue.config.js ./
COPY ./babel.config.js ./
COPY ./vue-file-import.d.ts ./
RUN npm install
CMD npm run serve -- --port 8081
# CMD bash
