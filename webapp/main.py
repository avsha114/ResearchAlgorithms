# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import csv

from flask import Flask, render_template, request, flash, redirect, url_for
import json
from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, TextAreaField
from wtforms.validators import InputRequired
import os
from prtpy.bins import BinsKeepingContents
from prtpy.packing.bin_completion import bin_completion

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# This form is used for the algorithms input
class DataForm(FlaskForm):
    binsize = IntegerField("BinSize:", validators=[InputRequired()])
    items = TextAreaField('Items (divided by spaces):', validators=[InputRequired()], render_kw={'class': 'form-control', 'rows': 7})
    submit = SubmitField('Compute')


# This form is simply for a 'Return Home' button with styling
class HomeForm(FlaskForm):
    submit = SubmitField('Return Home')


# This function is our home page. The user should insert the input here.
@app.route('/', methods=['GET', 'POST'])
def run():
    input_form = DataForm()
    is_submitted = input_form.validate_on_submit()

    if not is_submitted:
        return render_template('index.html', form=input_form)
    else:
        try:
            binsize = input_form.binsize.data
            items_str = input_form.items.data.split()
            items = [int(s) for s in items_str]
            result = bin_completion(BinsKeepingContents(), binsize, items)

            # Results page:
            return redirect(url_for(apply.__name__, binsize=binsize, items=items.__str__(), result=result.bins.__str__()))
        except Exception:
            # Error page:
            return render_template('fail.html', form=HomeForm())


# Results page:
@app.route('/results', methods=['GET', 'POST'])
def apply():
    result = json.loads(request.args['result'])
    binsize = request.args['binsize']
    input_items = request.args['items']

    return render_template('result.html', form=HomeForm(), len=len(result), result=result, alg_input=f"Binsize: {binsize} | Items: {input_items}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
