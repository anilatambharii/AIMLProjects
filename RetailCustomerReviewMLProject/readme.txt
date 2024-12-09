Building and Deploying a Production Machine Learning Solution

Use Case: Design and deploy an AI-driven natural language processing (NLP) solution to classify and analyze customer feedback for a client in the retail industry.

Design

Objective: Use AI to analyze customer reviews and categorize them into themes like product quality, service experience, and delivery issues.
Architecture:

Frontend: A web interface for users to upload customer reviews and view insights.

Backend:
NLP model for sentiment and thematic classification.
REST API to interact with the model.

Infrastructure: Containerized deployment using Docker on AWS with Kubernetes for scaling.

Tools:

NLP: Hugging Face Transformers (e.g., BERT).
Deployment: FastAPI for API development, AWS for hosting.
Monitoring: Prometheus and Grafana for API and model monitoring.

# Retail Customer Review NLP Model & API

This repository contains code for training a Natural Language Processing (NLP) model using the BERT architecture to classify retail customer reviews, and deploying it via a FastAPI web service to analyze new reviews.

## Table of Contents

- [Overview](#overview)
- [File Descriptions](#file-descriptions)
  - [TrainNLPModel.py](#TrainNLPModelpy)
  - [DeploymentAPI.py](#DeploymentAPIpy)
  - [analyze.py](#analyzepy)
- [Setup and Installation](#setup-and-installation)
- [Running the Application](#running-the-application)
  - [Training the Model](#training-the-model)
  - [Running the API](#running-the-api)
  - [Testing the API](#testing-the-api)
- [Troubleshooting](#troubleshooting)

## Overview

This project includes the following:

1. **Training a BERT-based text classification model** on a subset of the Yelp review dataset.
2. **Deploying the trained model as an API** using FastAPI to classify new reviews into one of the predefined categories.
3. **A Python script to interact with the deployed API** to analyze new customer reviews.

## File Descriptions

### `TrainNLPModel.py`

This file is responsible for training a BERT-based model for classifying retail customer reviews. It follows these steps:

- Loads a subset of the Yelp Review dataset (`train[:100]` and `train[100:200]`).
- Tokenizes the reviews using the BERT tokenizer.
- Fine-tunes the `bert-base-uncased` model on the Yelp review dataset.
- Saves the model and tokenizer to a local directory (`./results`).

Key Libraries:
- `transformers`: Used to load and train the BERT model.
- `datasets`: Used to load the Yelp Review dataset.
- `torch`: Used for deep learning and model training.

#### Example Usage:
```bash
python TrainNLPModel.py
