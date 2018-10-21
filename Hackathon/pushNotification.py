from pyfcm import FCMNotification
from jsonParser import get_source
push_service = FCMNotification(api_key="<api-key>")

# OR initialize with proxies
def sendNotification():
    proxy_dict = {
          "http"  : "http://127.0.0.1",
          "https" : "http://127.0.0.1",
        }
    push_service = FCMNotification(api_key="AIzaSyA8VwXcQ2S4Ar7Ps-3JueYkD0kFgK52sso", proxy_dict=proxy_dict)

    # Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging

    registration_id = "WIg9eFUP4A:APA91bELByRRfe17jrhzmj6MTJBXkXV5CSyqSLbFcFi2DvF1gix9gL-v7W9vGa8gPup29ahQ0UFLwCjVBpDzoshYYaJVaOuWWhiQ9p0V2-n6qlyCGwyfJbBoS5q2udv-DiQJhTOLX30F>"
    message_title = "Emergency"
    message_body = "Pickup at",get_source()
    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)


    print(result)