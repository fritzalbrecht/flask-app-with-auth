# Deploy Python Flask App with SAML Authenticatoin
---

This repo features a very simple Flask app that demonstrates a successful usage of SAML authentication using a Google Workspace app for SAML authentication. The webapp is hosted at:

https://flaskapp.fritzalbrecht.com

Google Workspace was chosen because it features an enterprise grade SAML solution and offers a wide variety of tools and features.

The Flask app is configured to be run on ECS Fargate to minimize infrastructure overhead. To deploy the infrastructure you simply need to apply the terraform config. Note; the terraform config is based off the config found in this repo https://github.com/aws-samples/deploy-python-flask-microservices-to-aws-using-open-source-tools except it has been updated to use ECS Fargate instead of EC2 on ECS using auto scaling groups.

To run the app a Dockerfile needs to be built using the app.py code in the /app directory.

The ECS configuration is configured in terraform and can be found in the /terraform directory. This also features the usage of Cloudflare DNS to allow the Flask app to be accessed over HTTPS.

The /scripts directory also features both an onboarding and an offboarding script to allow quick and potentially automated ways of provisioning user access for the SAML app. OAuth2 credentials will be needed in order to access the Google Workspace Admin SDK API. More info on this API can be found here: https://developers.google.com/admin-sdk/reference-overview

Examples of how to use the scripts are below:

python3 onboard.py --first <first_name> --last <last_name>

python3 onboard.py --email <email_address>

