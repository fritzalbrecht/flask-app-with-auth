from flask import Flask, request, redirect, render_template, make_response, session
from onelogin.saml2.auth import OneLogin_Saml2_Auth
import json
import os

app = Flask(__name__)
app.secret_key = "12345678901"  # Replace with your secret key or use os.urandom(24)

def init_saml_auth(req):
    # Load SAML settings from file
    saml_settings = json.load(open(os.path.join(os.path.dirname(__file__), 'saml', 'settings.json')))
    return OneLogin_Saml2_Auth(req, old_settings=saml_settings)

def prepare_flask_request():
    # Helper to construct the request for python-saml
    url_data = request.form if request.method == 'POST' else request.args
    return {
        'https': 'on' if request.scheme == 'https' else 'off',
        'http_host': request.host,
        'script_name': request.path,
        'server_port': request.environ.get('SERVER_PORT'),
        'get_data': url_data.copy(),
        'post_data': request.form.copy()
    }

@app.route('/')
def home():
    if session.get('authenticated'):
        return """
            <h1>Welcome to the Flask SAML App!</h1>
            <p>You are already authenticated.</p>
            <a href="/authenticated"><button>Go to Authenticated Page</button></a>
        """
    else:
        return """
            <h1>Welcome to the Flask SAML App!</h1>
            <form action="/saml/login" method="get">
                <button type="submit">Login via SAML</button>
            </form>
        """

@app.route('/saml/metadata')
def saml_metadata():
    req = prepare_flask_request()
    auth = init_saml_auth(req)
    settings = auth.get_settings()
    metadata = settings.get_sp_metadata()
    errors = settings.validate_metadata(metadata)
    if len(errors) == 0:
        response = make_response(metadata, 200)
        response.headers['Content-Type'] = 'text/xml'
        return response
    else:
        return "Error validating metadata: " + ', '.join(errors), 500

@app.route('/saml/login')
def saml_login():
    req = prepare_flask_request()
    auth = init_saml_auth(req)
    return redirect(auth.login())

@app.route('/saml/acs', methods=['POST'])
def saml_acs():
    req = prepare_flask_request()
    auth = init_saml_auth(req)
    auth.process_response()
    errors = auth.get_errors()
    if len(errors) == 0:
        # SAML authentication successful. Retrieve attributes as needed.
        session_index = auth.get_session_index()
        user_data = auth.get_attributes()
        # Store authentication flag and user attributes in session
        session['authenticated'] = True
        session['user_data'] = user_data
        return redirect('/')
    else:
        return "SAML Authentication Error: " + ", ".join(errors), 500

@app.route('/authenticated')
def authenticated():
    if not session.get('authenticated'):
        return redirect('/')
    # Sample content for authenticated users with a logout button
    return """
        <h1>Authenticated Page</h1>
        <p>Welcome, you have successfully authenticated via SAML.</p>
        <p>User Data: {}</p>
        <form action="/logout" method="get">
            <button type="submit">Logout</button>
        </form>
    """.format(session.get('user_data'))

@app.route('/logout')
def logout():
    # Clear the user session
    session.clear()
    # Return a logout page with a SAML login button
    return """
        <h1>You have been logged out.</h1>
        <form action="/saml/login" method="get">
            <button type="submit">Login via SAML</button>
        </form>
    """

if __name__ == "__main__":
    app.run(debug=True, ssl_context='adhoc')
