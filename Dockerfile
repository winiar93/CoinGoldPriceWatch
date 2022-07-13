# Specify a base image

FROM node:alpine

WORKDIR '/app'
# mv files to docker
COPY package.json .

# req
RUN npm install

COPY . .

# Default command
CMD ["npm", "start"]

