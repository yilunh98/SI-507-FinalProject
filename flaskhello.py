from flask import Flask,render_template, request
from readJson import retrieveFunds, retrieveManagers

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('welcome.html')

@app.route('/options')
def options():
    return render_template('options.html')

@app.route('/types')
def types():
    return render_template('types.html', data=retrieveFunds().keys())

@app.route('/handle_form_types', methods=['POST'])
def handle_form_types():
    funds_data = retrieveFunds()
    types = request.form["types"]
    if types == "":
        return render_template('rankings.html', data=funds_data)
    else:
        funds_data = funds_data[types]
        return render_template('typeResult.html', data=funds_data)


@app.route('/funds')
def funds():
    return render_template('funds.html', data=retrieveFunds())

@app.route('/handle_form_funds', methods=['POST'])
def handle_form_funds():
    funds_data = retrieveFunds()
    funds = request.form["funds"]
    if funds == "":
        return render_template('rankings.html', data=funds_data)
    else:
        if funds in funds_data['OE']:
            funds_data = funds_data['OE'][funds]
        else:
            if funds in funds_data['ET']:
                funds_data = funds_data['ET'][funds]
        return render_template('fundResult.html', data=funds_data)


@app.route('/managers')
def managers():
    return render_template('manager.html', data=retrieveManagers().keys())

@app.route('/handle_form_managers', methods=['POST'])
def handle_form_managers():
    managers_data = retrieveManagers()
    funds_data = retrieveFunds()
    managers = request.form["managers"]

    if managers == "":
        return render_template('rankings.html', data=funds_data)
    else:
        info = managers_data[managers]['info']
        fundsList = managers_data[managers]['fund']
        data = [info]
        for f in fundsList:
            if f in funds_data['OE']:
                    data.append(funds_data['OE'][f])
            else:
                if f in funds_data['ET']:
                    data.append(funds_data['ET'][f])
        return render_template('managersResult.html', data=data)


@app.route('/rankings')
def rankings():
    return render_template('rankings.html', data=retrieveFunds())


if __name__ == '__main__':
    print('starting Flask app', app.name)
    app.run(debug=True)
