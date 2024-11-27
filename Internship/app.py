from flask import Flask, render_template, request
import pickle
import pandas as pd

# Initialize Flask app
app = Flask(__name__)

# Load the model from the pickle file
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Define the route for the homepage
@app.route('/')
def home():
    return render_template('index.html')

# Define the route to handle form submission and make predictions
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data with correct field names
        quiz_total = float(request.form['quiz_total'])
        attendance = float(request.form['attendance'])
        grand_total = float(request.form['grand_total'])
        
        # Create DataFrame for the model
        data = pd.DataFrame([[quiz_total, attendance, grand_total]],
                            columns=['Total', 'Attendance %', 'Grand Total'])

        # Make prediction
        prediction = model.predict(data)[0]

        # Convert prediction to 'Pass' or 'Not Eligible'
        result = "Pass" if prediction == 1 else "Not Eligible"

        # Render the result page with the prediction
        return render_template('result.html', prediction=result)
    except KeyError as e:
        # Handle missing form data
        return f"Missing field in form submission: {e}", 400
    except ValueError:
        # Handle invalid input values
        return "Invalid input! Please enter valid numeric values.", 400

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
