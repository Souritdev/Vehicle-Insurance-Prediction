🚗 Vehicle Insurance Prediction -- MLops Project 🧑‍💻
End-to-end Automation of Machine Learning Workflows: Data ➡️ Model ➡️ CI/CD ➡️ Cloud
Delivering Robust, Scalable ML Solutions—Ready for the Real World!

📦 Project Features
Template Creation (template.py): Scaffold new ML projects with a single command.

Modular Package Setup (setup.py, pyproject.toml): Easily import and manage local packages.

Virtual Environment and Requirements Management:

bash
conda create -n vehicle python=3.10 -y
conda activate vehicle
pip install -r requirements.txt
pip list
Comprehensive MongoDB Data Pipeline: Secure cloud database integration, push key-value data, and visualize results.

Robust Logging & Exception Handling: Centralized utilities for error-free tracking.

Notebook-Driven EDA & Feature Engineering: Powerful data exploration and transformation in Jupyter.

Scalable Data Ingestion Module: Connect, transform, and load data from MongoDB with custom configurations.

Seamless Cloud Integration: AWS setup and S3 storage for models and artifacts.

Automated CI/CD Pipeline:

Dockerized deployments

GitHub Actions & Self-Hosted Runner

ECS, EC2 & ECR setup

Prediction API & App: FastAPI/Flask app with /training and dynamic prediction endpoints.

Secure Secrets Management: Environment variable configuration for AWS/GitHub.

Live Monitoring and Retraining: Trigger model updates, check health, and performance metrics.

🛠️ Project Setup
bash
# 1. Scaffold project template
python template.py

# 2. Setup Python project for local imports
# Reference: crashcourse.txt

# 3. Environment & Installation
🚗 Vehicle MLops Project
End-to-end Automation of Machine Learning Workflows: Data ➡️ Model ➡️ CI/CD ➡️ Cloud
Delivering Robust, Scalable ML Solutions—Ready for the Real World!

📦 Project Features
Template Creation (template.py): Scaffold new ML projects with a single command.

Modular Package Setup (setup.py, pyproject.toml): Easily import and manage local packages.

Virtual Environment and Requirements Management:

bash
conda create -n vehicle python=3.10 -y
conda activate vehicle
pip install -r requirements.txt
pip list
Comprehensive MongoDB Data Pipeline: Secure cloud database integration, push key-value data, and visualize results.

Robust Logging & Exception Handling: Centralized utilities for error-free tracking.

Notebook-Driven EDA & Feature Engineering: Powerful data exploration and transformation in Jupyter.

Scalable Data Ingestion Module: Connect, transform, and load data from MongoDB with custom configurations.

Seamless Cloud Integration: AWS setup and S3 storage for models and artifacts.

Automated CI/CD Pipeline:

Dockerized deployments

GitHub Actions & Self-Hosted Runner

ECS, EC2 & ECR setup

Prediction API & App: FastAPI/Flask app with /training and dynamic prediction endpoints.

Secure Secrets Management: Environment variable configuration for AWS/GitHub.

Live Monitoring and Retraining: Trigger model updates, check health, and performance metrics.

🛠️ Project Setup
bash
# 1. Scaffold project template
python template.py

# 2. Setup Python project for local imports
# Reference: crashcourse.txt

# 3. Environment & Installation
conda create -n vehicle python=3.10 -y
conda activate vehicle
pip install -r requirements.txt

# 4. Confirm Installation

# 4. Confirm Installation
pip list
🗄️ MongoDB Cloud Connection
Sign up for MongoDB Atlas

Create Cluster (M0, default settings)

Setup DB User (+ Network Access: 0.0.0.0/0)

Get Connection String for Python >= 3.6

Use and store the MongoDB URI securely (via ENV VARIABLE)

bash
🗄️ MongoDB Cloud Connection
Sign up for MongoDB Atlas

Create Cluster (M0, default settings)

Setup DB User (+ Network Access: 0.0.0.0/0)

Get Connection String for Python >= 3.6

Use and store the MongoDB URI securely (via ENV VARIABLE)

bash
# For Bash
export MONGODB_URL="mongodb+srv://<username>:<password>@cluster-url"

# For PowerShell
$env:MONGODB_URL="mongodb+srv://<username>:<password>@cluster-url"
See .gitignore for excluded artifacts.

📝 Notebooks & Logging
MongoDB Demo: notebook/mongoDB_demo.ipynb

EDA & Feature Engg: Explore, visualize, and preprocess datasets.

Logger & Exception: Centralized error handlers, tested in demo.py.

🧩 Data Ingestion & Validation
Declare configs in constants/__init__.py

Flexible MongoDB connection module: configuration/mongo_db_connections.py

Fetch, transform, and load data into pandas DataFrames.

Data Validation: Schema management in config/schema.yaml

Utils: main_utils.py for reusable helpers.

⚙️ Data Transformation & Model Trainer
Modular workflow for ingestion, validation, transformation, and training.

AWS S3 Integration:

aws_connection.py for S3 operations

Model, artifact bucket config in constants

Push/pull models via entity/s3_estimator.py

Model Evaluation & Pusher: Compare, threshold, and deploy automatically.

🚀 CI/CD Pipeline & Cloud Deployments
Docker Integration: Dockerfile & .dockerignore

Github Actions: .github/workflows/aws.yaml

Self-hosted EC2 Runner: Connect Github to EC2 for scalable builds.

ECR & EC2 Setup:

Store images in AWS ECR

Launch app on EC2

Port forward (5080) for live access.

🌐 Prediction API
app.py: FastAPI/Flask routes

/training : Automate model training

/predict : Deploy and query predictions

🔒 Secrets & Environment Variables
Store sensitive credentials as environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, ECR_REPO).

Configure via Github Secrets:

Repo → Settings → Secrets and Variables → NewRepoSecret

export MONGODB_URL="mongodb+srv://<username>:<password>@cluster-url"

# For PowerShell
$env:MONGODB_URL="mongodb+srv://<username>:<password>@cluster-url"
See .gitignore for excluded artifacts.

📝 Notebooks & Logging
MongoDB Demo: notebook/mongoDB_demo.ipynb

EDA & Feature Engg: Explore, visualize, and preprocess datasets.

Logger & Exception: Centralized error handlers, tested in demo.py.

🧩 Data Ingestion & Validation
Declare configs in constants/__init__.py

Flexible MongoDB connection module: configuration/mongo_db_connections.py

Fetch, transform, and load data into pandas DataFrames.

Data Validation: Schema management in config/schema.yaml

Utils: main_utils.py for reusable helpers.

⚙️ Data Transformation & Model Trainer
Modular workflow for ingestion, validation, transformation, and training.

AWS S3 Integration:

aws_connection.py for S3 operations

Model, artifact bucket config in constants

Push/pull models via entity/s3_estimator.py

Model Evaluation & Pusher: Compare, threshold, and deploy automatically.

🚀 CI/CD Pipeline & Cloud Deployments
Docker Integration: Dockerfile & .dockerignore

Github Actions: .github/workflows/aws.yaml

Self-hosted EC2 Runner: Connect Github to EC2 for scalable builds.

ECR & EC2 Setup:

Store images in AWS ECR

Launch app on EC2

Port forward (5080) for live access.

🌐 Prediction API
app.py: FastAPI/Flask routes

/training : Automate model training

/predict : Deploy and query predictions

🔒 Secrets & Environment Variables
Store sensitive credentials as environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, ECR_REPO).

Configure via Github Secrets:

Repo → Settings → Secrets and Variables → NewRepoSecret