

import flask
import pickle
import pandas as pd


# Use pickle to load in the pre-trained model
# to load model
rf_model_file_loaded=r'C:\Users\armifaizal\Google Drive\360DIGITMG DATA SCIENCE COURSE\DATA SCIENCE LIVE PROJECT 2\WEBAPP\model\rf_optimized.pkl'
rf_model=pickle.load(open(rf_model_file_loaded, 'rb'))

# Initialise the Flask app
app = flask.Flask(__name__, template_folder='templates')

# Set up the main route
@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('main.html'))
    
    if flask.request.method == 'POST':
        # Extract the input
        adaptability = flask.request.form['Adaptability and Intiative']
        attendance = flask.request.form['Attendance and Punctuality ']
        self_eval = flask.request.form['Self Evaluation ']

        # Make DataFrame for model
        input_variables = pd.DataFrame([[adaptability, attendance, self_eval]],
                                       columns=['Adaptability and Intiative', 'Attendance and Punctuality ', 'Self Evaluation '],
                                       dtype=float,
                                       index=['input'])

        # Get the model's prediction
        prediction = rf_model.predict(input_variables)[0]
        if prediction == 0:
            prediction = 'Will not resign'
        else:
            prediction = 'Will resign'
            
                
        # Render the form again, but add in the prediction and remind user
        # of the values they input before
        return flask.render_template('main.html',
                                     original_input={'Adaptability and Intiative':adaptability,
                                                     'Attendance and Punctuality ':attendance,
                                                     'Self Evaluation ':self_eval},
                                     result=prediction,
                                     )

if __name__ == '__main__':
    app.run()