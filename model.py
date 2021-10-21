import urllib
import sys
from urllib import request
import base64
from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import predict


def logo_detection(
        project: str,
        endpoint_id: str,
        filename: str,
        location: str = "us-central1",
        api_endpoint: str = "us-central1-aiplatform.googleapis.com",
):
    # regional API endpoints required.
    client_options = {"api_endpoint": api_endpoint}
    # Initialize client
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    with open(filename, "rb") as f:
        file_content = f.read()

    # format should be the same as the model's input schema.
    encoded_content = base64.b64encode(file_content).decode("utf-8")
    instance = predict.instance.ImageObjectDetectionPredictionInstance(
        content=encoded_content,
    ).to_value()
    instances = [instance]
    parameters = predict.params.ImageObjectDetectionPredictionParams(
        max_predictions=10,
    ).to_value()
    endpoint = client.endpoint_path(
        project=project, location=location, endpoint=endpoint_id
    )
    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )
    print("response")
    print(" deployed_model_id:", response.deployed_model_id)
    predictions = response.predictions
    for prediction in predictions:
        with open('phishing.csv', 'a') as f:
            if prediction["confidences"] >= .100:
                print(" prediction:", dict(prediction["confidences"]), file=f)
            else:
                print("nothin' boss")


# resolve a text file containing a list of hostnames
fList = sys.argv[1]
with open(fList, "r", encoding='utf-8-sig') as ins:
    for line in ins:
        urllib.request.urlretrieve(
            "https://website-screenshot.whoisxmlapi.com/api/v1?apiKey=$APIKEY&credits=DRS"
            "&fullPage=1&url={0}".format(line),
            "pic.jpg")
        logo_detection(project=$projectID, endpoint_id=$endpointID,
                                                        location=$regionID, filename="pic.jpg")