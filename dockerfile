FROM python:3.12.4

# Set the working directory
WORKDIR /Medical_Chatbot

# Copy application files
COPY . /Medical_Chatbot

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# populate the database with initial data
RUN python app/populate_database.py

# Expose the FastAPI default port
EXPOSE 8000

# Start the application with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]