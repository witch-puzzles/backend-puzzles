from app.core import settings
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

class EmailUtil():
    staticmethod
    def send_email(to: str, sender: str, subject: str, content: str):
        # Configure API key authorization
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = settings.BREVO_API_KEY  # Replace with your API key

        # Create an instance of the API client
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

        # Email details
        email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": to}],
            sender={"email": sender},
            subject=subject,
            html_content=content
        )

        try:
            # Send the email
            response = api_instance.send_transac_email(email)
            print(response)  # Print the response for debugging
        except ApiException as e:
            print("Exception when calling Brevo API: %s\n" % e)
        
