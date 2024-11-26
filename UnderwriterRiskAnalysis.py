import os
from openai import OpenAI
from typing import List, Dict
import openai
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

class InsuranceUnderwritingAI:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.risk_model = None

    def generate_custom_prompt(self, context: str) -> str:
        prompt = f"""
        Based on the following insurance underwriting context, generate a detailed and specific prompt
        to gather necessary information for risk assessment:

        Context: {context}

        Generated Prompt:
        """
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}]
        )
        return response.choices[0].message.content.strip()

    def process_submission(self, submission_data: Dict) -> Dict:
        prompt = self.generate_custom_prompt("Assess insurance risk based on the following submission data")
        submission_text = "\n".join([f"{k}: {v}" for k, v in submission_data.items()])
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"Submission Data:\n{submission_text}\n\nRisk Assessment:"}
            ]
        )
        
        return {
            "submission_data": submission_data,
            "ai_assessment": response.choices[0].message['content'].strip()
        }

    def train_risk_model(self, historical_data: pd.DataFrame):
        X = historical_data.drop('risk_level', axis=1)
        y = historical_data['risk_level']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.risk_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.risk_model.fit(X_train, y_train)
        
        y_pred = self.risk_model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model Accuracy: {accuracy}")
        print(classification_report(y_test, y_pred))

    def predict_risk(self, submission_data: Dict) -> str:
        if self.risk_model is None:
            raise ValueError("Risk model not trained. Please train the model first.")
        
        submission_df = pd.DataFrame([submission_data])
        risk_prediction = self.risk_model.predict(submission_df)[0]
        return risk_prediction

    def assess_potential_losses(self, submission_data: Dict) -> Dict:
        prompt = """
        Based on the following insurance submission data, assess potential losses and predict risk scenarios:

        Submission Data:
        """
        for key, value in submission_data.items():
            prompt += f"{key}: {value}\n"
        
        prompt += "\nPotential Losses and Risk Scenarios:"
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"{submission_data}"}
            ]
        )
        
        return {
            "submission_data": submission_data,
            "loss_assessment": response.choices[0].message['content'].strip()
        }

# Usage example
if __name__ == "__main__":
    ai_underwriter = InsuranceUnderwritingAI()
    
    context = "Home insurance policy for a coastal property"
    custom_prompt = ai_underwriter.generate_custom_prompt(context)
    print(f"Custom Prompt: {custom_prompt}")
    
    # Process submission
    submission = {
        "property_type": "Single-family home",
        "location": "Coastal area",
        "construction_year": 1995,
        "square_footage": 2500,
        "previous_claims": 1
    }
    assessment = ai_underwriter.process_submission(submission)
    print(f"AI Assessment: {assessment['ai_assessment']}")
    
    # Train risk model (assuming you have historical data)
    historical_data = pd.read_csv("historical_underwriting_data.csv")
    ai_underwriter.train_risk_model(historical_data)
    
    # Predict risk for new submission
    risk_level = ai_underwriter.predict_risk(submission)
    print(f"Predicted Risk Level: {risk_level}")
    
    # Assess potential losses
    loss_assessment = ai_underwriter.assess_potential_losses(submission)
    print(f"Loss Assessment: {loss_assessment['loss_assessment']}")