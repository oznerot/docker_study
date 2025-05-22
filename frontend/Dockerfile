#Angular Dockerfile
FROM node:20.19.2 AS build

WORKDIR /app

COPY ./crud-student/package*.json .
RUN npm install

COPY ./crud-student .
RUN npm run build --prod

FROM nginx:alpine

COPY --from=build /app/dist/crud-student/browser /usr/share/nginx/html
COPY ./crud-student/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80   

CMD ["nginx", "-g", "daemon off;"]