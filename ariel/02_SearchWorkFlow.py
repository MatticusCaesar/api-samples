# This is the typical way to query to the ArielAPI, and receive
# the results. ArielAPI searches are asynchronous. 
# Endpoints are used to determine if the search has completed.
# After determining that the search is complete, call 
# GET /searches/{searchID}/results for search results.
# The results are saved through the POST /searches/{searchID} endpoint.

def main():
    import sys, os
    sys.path.append(os.path.realpath('../modules'))
    import json
    from arielapiclient import APIClient

    # Creates instance of APIClient. It contains all of the API methods.
    api_client = APIClient()

    # This is the AQL expression to send for the search.
    query_expression = "SELECT distinct sourceIP from events"
    

    # Use the query parameters above to call a method. This will call
    # POST /searches on the Ariel API. (look at arielapiclient for more
    # detail).  A response object is returned. It contains  
    # successful or not successful search information.
    # The searchID corresponding to this search is contained in
    # the JSON object.

    print("Making POST request to /ariel/searches.\n")

    response = api_client.create_search(query_expression, '2')

    # Each response contains an HTTP response code.
    # Response codes in the 200 range indicate that your request succeeded.
    # Response codes in the 400 range indicate that your request failed due to
    # incorrect input.
    # Response codes in the 500 range indicate that there was an error on the
    # server side.
    print("Response code for this request is: " + str(response.code))
    

    # The search is asynchronous, so the response will not be the results of 
    # the search.

    # The 2 lines below parse the body of the response (a JSON object)
    # into a dictionary, so we can discern information, such as the searchID.

    print("\nThis is the reponse body: ")
    response_json = json.loads(response.read().decode('utf-8'))

    # Prints the contents of the dictionary.
    print(response_json)

    # Retrieves the searchID of the query from the dictionary.

    print("\nRetrieving results of your search...")
    search_id = response_json['searchID']

    # This block of code calls GET /searches/{searchID} on the Ariel API
    # to determine if the search is complete. This block of code will repeat
    # until the status of the search is 'COMPLETE' or there is an error.
    response = api_client.get_search(search_id)
    error = False
    while (response_json['status'] != 'COMPLETED') and not error:
        if (response_json['status'] == 'EXECUTE') | \
                (response_json['status'] == 'SORTING') | \
                (response_json['status'] == 'WAIT'):
            response = api_client.get_search(search_id)
            response_json = json.loads(response.read().decode('utf-8'))
        else:
            print(response_json['status'])
            error = True

    # After the search is complete, call the GET /searches/{searchID} to obtain
    # the result of the search. 
    # Depending on whether the "application/json" or "application/csv" 
    # method is given, return search results will be in JSON form or CSV form.
    response = api_client.get_search_results(
        search_id, 'application/json', '1', '11')

    body = response.read().decode('utf-8')
    body_json = json.loads(body)

    print("\nHere are the results of your search in JSON: ")
    # This is for pretty printing the JSON object.
    print(json.dumps(body_json, indent=2, separators=(',', ':')))

    # This is the same call as before, but asks for a CSV object in return.

    print("\nHere are the results of your search in CSV: ")
    response = api_client.get_search_results(search_id, "application/csv")
    print("\n"+response.read().decode('utf-8'))

if __name__ == "__main__":
    main()