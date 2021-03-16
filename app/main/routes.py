from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def homepage():
    return render_template('main/home.html')


# Create Party
@main.route('/create_party', methods=['GET', 'POST'])
def create_party():
    pass