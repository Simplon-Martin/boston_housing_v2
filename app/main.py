from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
import xgboost as XGB
from app.models import User, Estimation
import datetime
import pickle
import pandas as pd

from app.db import db
from app.forms import PredictForm

main = Blueprint('main', __name__)


@main.route('/')
def index():
    form = PredictForm()
    return render_template('index.html', form=form, current_user=current_user)


@main.route('/predict', methods=['POST', 'GET'])
def predict():
    model = load_model()
    rm = float(request.form['rm'])
    lstat = float(request.form['lstat'])
    ptratio = float(request.form['ptratio'])

    d = {'RM': [rm], 'LSTAT': [lstat], 'PTRATIO': [ptratio]}
    res = pd.DataFrame(data=d)

    prediction = model.predict(res)

    formate_pred = "{:.2f}".format(prediction[0])

    if current_user.is_authenticated:
        new_estimation_with_user = Estimation.Estimation(user_id=current_user.id, estimation=prediction[0], rm=rm, lstat=lstat, ptratio=ptratio)
        db.session.add(new_estimation_with_user)
        db.session.commit()

    return render_template('predict.html', prediction=formate_pred)


@main.route('/profile')
@login_required
def profile():

    user_estimations = db.session.query(Estimation.Estimation).filter(
        Estimation.Estimation.user_id == current_user.id).all()

    if not user_estimations:
        form = PredictForm()
        return render_template('index.html', form=form, current_user=current_user)
    else:
        return render_template('profile.html', name=current_user.name, user_estimations=user_estimations)


def load_model():
    # Load the saved model
    with open('app/model/model_boston_housing_v2.pkl', 'rb') as file:
        model = pickle.load(file)

    return model
