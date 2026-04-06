#Use Python base image
FROM python:3.9-slim

#set working directory
WORKDIR /app

#Copy requirements file
COPY requirements.txt ./

#Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

#Copy everything else
COPY . .

#Expose FastAPI port
EXPOSE 8000

#Run the application
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]