# This sample demonstrates how to use query parameters with a REST API endpoint.

# For a list of the endpoints that you can use along with the parameters that
# they accept you can view the REST API interactive help page on your
# deployment at https://<hostname>/restapi/doc
# You can also retrieve a list of available endpoints through the API itself
# at the /api/help/capabilities endpoint.

import sys, os
sys.path.append(os.path.realpath('../modules'))
from RestApiClient import RestApiClient
import SampleUtilities as SampleUtilities
import Cleanup

def main():
    # For the purpose of this sample, the reading in of credentials, the setup
    # of HTTP request headers, and the construction and sending of a request
    # object has been abstracted to the 'RestApiClient' class.
    # For more information on how these operations are done see the sample
    # '01_Authentication.py'.
    client = RestApiClient()
    
    # Many API endpoints accept parameters.
    # One type of parameter is a query parameter.
    # If an endpoint accepts query parameters they are passed after a '?' as
    # part of the URL. Each parameter has a name and a value separated by a '='.
    # Several parameters can be passed separated by '&' characters.
    SampleUtilities.pretty_print_request(client, 'referencedata/sets?name=rest_api_samples_testset&elementType=ALN', 'POST')
    
    response = client.call_api('referencedata/sets?name=rest_api_samples_testset&elementType=ALN', 'POST')
    
    # The response code for successfully creating a set is 201.
    if (response.code == 201):
        SampleUtilities.pretty_print_response(response)
    # The error code that occurs when attempting to create a set that already
    # exists is 409.
    elif (response.code == 409):
        print("Reference set already exists")
        response = client.call_api('referencedata/sets/rest_api_samples_testset', 'GET')
        SampleUtilities.pretty_print_response(response)
    elif (response.code >= 500):
        print("An internal server error occurred. You should check your system.")
        SampleUtilities.pretty_print_response(response)
    else:
        print("Some other error has occurred:")
        SampleUtilities.pretty_print_response(response)


    # You can uncomment this line to have this script remove the data it
    # creates after it is done, or you can invoke the Cleanup script directly:
    #Cleanup.cleanup_introduction_data(client)


if __name__ == "__main__":
    main()
