from flask import Flask, make_response, jsonify, request
from flask_restful import Api, Resource
from flask_cors import CORS
import sib_api_v3_sdk
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
api = Api(app)

class Index(Resource):
    def get(self):
        return make_response(jsonify({"message": "Welcome to the email API"}))
    
api.add_resource(Index, "/")

class SendEmail(Resource):

    def post(self):
        try:
            # Capturing the data from the form
            name = request.json["name"]
            email = request.json["email"]
            subject = request.json["subject"]
            message = request.json["message"]
            to_email = request.json["toEmail"]

            # Function to send the email
            configuration = sib_api_v3_sdk.Configuration()
            configuration.api_key["api-key"] = os.environ["SENDINBLUE_API_KEY"]
            api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

            # Defining the email parameters
            sender = {"name": name, "email": email}
            to = [{"email": to_email}]
            email_content = message

            send_email = sib_api_v3_sdk.SendSmtpEmail(to=to, html_content=email_content, sender=sender, subject=subject)

            api_instance.send_transac_email(send_email)

            return make_response(jsonify({"success": "Email sent successfully!"}), 200)

        except Exception as e:
            print(e)  # Print the exception to the console for debugging
            return make_response(jsonify({"error": str(e)}), 500)

api.add_resource(SendEmail, "/send-email")

if __name__ == "__main__":
    app.run(port=5555, debug=True)
