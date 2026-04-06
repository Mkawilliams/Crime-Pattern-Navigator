FROM node:18

#Set working directory
WORKDIR /app

#Copy package.json and package-lock.json
COPY package*.json ./

#Install dependencies
RUN npm install 
RUN npm install leaflet react-leaflet

#Cop everything else
COPY . .

#Expose port
EXPOSE 3000

#Default command
CMD ["npm", "start"]