FROM node:alpine

ENV PORT 3000

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY package*.json yarn.lock /usr/src/app/
RUN yarn install

COPY . /usr/src/app

RUN yarn run build
EXPOSE 3000

CMD ["yarn", "run", "dev"]
