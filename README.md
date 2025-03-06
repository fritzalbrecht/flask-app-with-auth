# Deploy Python Flask App with SAML Authenticatoin
---


# Services Used
---

This repo features a very simple Flask app that demonstrates a successful usage of SAML authentication using a Google Workspace app for SAML authentication.

Google Workspace was chosen because it features an enterprise grade SAML solution and offers a wide variety of tools and features.

The Flask app is configured to be run on ECS Fargate to minimize infrastructure overhead. To run the app a Dockerfile needs to be built using the app.py code in the /app directory.

The ECS configuration is configured in terraform and can be found in the /terraform directory. This also features the usage of Cloudflare DNS to allow the Flask app to be accessed over HTTPS.

The /scripts directory also features both an onboarding and an offboarding script to allow quick and potentially automated ways of provisioning user access for the SAML app. OAuth2 credentials will be needed in order to access the Google Workspace Admin SDK API. More info on this API can be found here: https://developers.google.com/admin-sdk/reference-overview

Examples of how to use the scripts are below:

python3 onboard.py --first <first_name> --last <last_name>

python3 onboard.py --email <email_address>

