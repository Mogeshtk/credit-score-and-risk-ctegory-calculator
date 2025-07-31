from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

def calculate_credit_score(payment_delay, past_due, credit_limit, bounced_cheques, years_with_salcomp):
    score = (
        ((1 - min(payment_delay / 90, 1)) * 300) +
        ((1 - min(past_due / credit_limit, 1)) * 250) +
        ((1 - min(bounced_cheques / 10, 1)) * 150) +
        (min(years_with_salcomp / 10, 1) * 150)
    )
    return round(min(max(score, 300), 850))

def assign_risk(score):
    if score >= 800:
        return 'Excellent'
    elif score >= 740:
        return 'Very Good'
    elif score >= 670:
        return 'Good'
    elif score >= 580:
        return 'Fair'
    else:
        return 'Poor'

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    payment_delay = float(data.get('payment_delay', 0))
    past_due = float(data.get('past_due', 0))
    credit_limit = float(data.get('credit_limit', 1))
    bounced_cheques = float(data.get('bounced_cheques', 0))
    years_with_salcomp = float(data.get('years_with_salcomp', 0))
    score = calculate_credit_score(payment_delay, past_due, credit_limit, bounced_cheques, years_with_salcomp)
    risk = assign_risk(score)
    return jsonify({"credit_score": score, "risk_category": risk})

if __name__ == "__main__":
    # Running on http://127.0.0.1:5000/
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))