# bitsMtech_MLOps_Assignment_2

This project is designed to provide an inference service for making predictions using a machine learning model. Below are the details regarding the structure, setup, and usage of the application.

## Project Structure

```
bitsMtech_MLOps_Assignment_2
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── executionSteps.txt
│   ├── api
│   │   └── routes.py
│   ├── core
│   │   └── config.py
│   ├── models
│   │   └── model.py
│   ├── schemas
│   │   ├── __init__.py
│   │   └── prediction.py
│   └── services
│       └── inference.py
├── Dockerfile
├── requirements.txt
├── .dockerignore
└── README.md
```

## Setup Instructions

1. **Clone the Repository**
   Clone this repository to your local machine using:
   ```
   git clone <repository-url>
   ```

2. **Navigate to the Project Directory**
   ```
   cd bitsMtech_MLOps_Assignment_2
   ```

3. **Install Dependencies**
   Install the required Python packages listed in `requirements.txt`:
   ```
   pip install -r requirements.txt
   ```

## Docker Setup

### Dockerfile

The Dockerfile is configured to create a Docker image for the inference service. It uses a lightweight Python image and installs the necessary dependencies.

### Build and Run the Docker Image

To build and run the Docker image locally, follow these steps:

1. **Build the Docker Image**
   ```
   docker build -t inference-service .
   ```

2. **Run the Docker Container**
   ```
   docker run -p 5000:5000 inference-service
   ```

## Verify Predictions

Once the container is running, you can verify predictions using `curl` or Postman.

### Using curl

You can send a POST request to the inference service like this:
```
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{"data": "your_input_data"}'
```

### Using Postman

1. Set the request type to POST.
2. Enter the URL: `http://localhost:5000/predict`.
3. Set the body to raw JSON and provide your input data.

## Additional Information

Refer to `executionSteps.txt` for detailed execution steps and any additional instructions related to the application.