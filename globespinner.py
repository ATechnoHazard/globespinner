from python_terraform import *
from dispatcher import Dispatcher
from typing import List
import os

t = Terraform()
dispatcher = Dispatcher()

DO_PATH = os.path.join(os.curdir,  "configs", "digitalocean")
AWS_PATH = os.path.join(os.curdir,  "configs", "aws")
GC_PATH = os.path.join(os.curdir,  "configs", "gcp")

details = {}


class BotHandler(object):
    def usage(self) -> str:
        return '''
        This is a bot for deploying cloud resources using all the major cloud providers, including AWS, Azure, Google Cloud, Digital Ocean etc.
        '''

    def handle_message(self, message, bot_handler) -> None:
        split_text = message["full_content"].split()
        command = split_text[0]
        args = split_text[1:]

        if command.startswith("/"):
            dispatcher.dispatch(command, args, bot_handler, message)

        fulfillment_text, deploy = detect_intent_texts("globespinner-xwpvfo",
                                                       "12345678", message["full_content"], "en-US")
        bot_handler.send_reply(message, fulfillment_text)

        if deploy:
            if details["12345678"]["provider"] == "DigitalOcean":
                handle_do(bot_handler, message, args)
                return

            if details["12345678"]["provider"] == "Google Cloud":
                handle_gcp(bot_handler, message, args)
                return

            if details["12345678"]["provider"] == "Amazon Web Services":
                handle_aws(bot_handler, message, args)
                return

            if details["12345678"]["provider"] == "Microsoft Azure":
                bot_handler.send_reply(
                    message, "We currently don't support this provider.")
                return


handler_class = BotHandler


def handle_do(bot_handler, message, args: List[str]):
    t.init(DO_PATH)
    bot_handler.send_reply(message, "Creating your droplet...")
    deets = details["12345678"]

    return_code, stdout, stderr = t.apply(DO_PATH,
                                          vars={"image": deets["os"], "name": "Test-droplet", "size": get_instance_type("DigitalOcean", deets["memory"], deets["processor"]), "region": deets["region"]}, **{"skip_plan": True, "auto_approve": IsFlagged, "capture_output": True})

    if(stderr):
        bot_handler.send_reply(message, str(stderr))
    else:
        bot_handler.send_reply(message, str(stdout))

    return


def handle_aws(bot_handler, message, args: List[str]) -> None:
    t.init(AWS_PATH)
    deets = details["12345678"]
    bot_handler.send_reply(message, "Creating your ec2 instance...")
    return_code, stdout, stderr = t.apply(AWS_PATH, vars={"ami": deets["ami"]}, **{
            "skip_plan": True, "auto_approve": IsFlagged, "capture_output": True})

    if(stderr):
        bot_handler.send_reply(message, str(stderr))
    else:
        bot_handler.send_reply(message, str(stdout))


def handle_gcp(bot_handler, message, args: List[str]):
    t.init(GC_PATH)
    deets = details["12345678"]
    return_code, stdout, stderr = bot_handler.send_reply(message, "Creating your Compute instance...")
    t.apply(GC_PATH, vars={"region": deets["region"], "zone": deets["region"]+"b", "type": get_instance_type("Google Cloud", deets["memory"], deets["processor"]), "image": "ubuntu-os-cloud/ubuntu-1804-lts" }, **{"skip_plan": True,
                                 "auto_approve": IsFlagged, "capture_output": True})

    if(stderr):
        bot_handler.send_reply(message, str(stderr))
    else:
        bot_handler.send_reply(message, str(stdout))



def detect_intent_texts(project_id, session_id, text, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    import dialogflow_v2 as dialogflow
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    text_input = dialogflow.types.TextInput(
        text=text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)

    print('=' * 20)
    print('Query text: {}'.format(response.query_result.query_text))
    print('Detected intent: {} (confidence: {})\n'.format(
        response.query_result.intent.display_name,
        response.query_result.intent_detection_confidence))
    print('Fulfillment text: {}\n'.format(
        response.query_result.fulfillment_text))
    # print('Parameters: {}\n'.format(
    #     response.query_result.parameters))

    if(response.query_result.intent.display_name == "Deploy intent - digitalocean" and response.query_result.all_required_params_present):
        params = response.query_result.parameters
        details[session_id] = {}
        details[session_id]["provider"] = params["provider"]
        return response.query_result.fulfillment_text, False

    if(response.query_result.intent.display_name == "Get deployment details" and response.query_result.all_required_params_present):
        params = response.query_result.parameters
        details[session_id]["memory"] = params["memory"]
        details[session_id]["os"] = params["os"]
        details[session_id]["processor"] = params["processor"]
        details[session_id]["region"] = params["region"]
        return response.query_result.fulfillment_text, False

    if(response.query_result.intent.display_name == "Get deployment details - yes"):
        return response.query_result.fulfillment_text, True

    return response.query_result.fulfillment_text, False


def get_instance_type(provider: str, mem: str, cpu: str):
    resource = cpu + "-" + mem
    mappings = {"DigitalOcean": {}, "Google Cloud": {},
                "Amazon Web Services": {}}
    mappings["DigitalOcean"] = {
        "1vcpu-1gb": "s-1vcpu-1gb",
        "1vcpu-2gb": "s-1vcpu-2gb",
        "3vcpu-1gb": "s-3vcpu-1gb",
        "2vcpu-2gb": "s-2vcpu-2gb",
        "1vcpu-3gb": "s-1vcpu-3gb",
        "2vcpu-4gb": "s-2vcpu-4gb",
        "4vcpu-8gb": "s-4vcpu-8gb"
    }

    mappings["Google Cloud"] = {
        "1vcpu-614mb": "f1-micro",
        "1vcpu-1.7gb": "g1-small",
        "1vcpu-3.75gb": "n1-standard-1",
        "2vcpu-7.5gb": "n1-standard-2",
        "4vcpu-15gb": "n1-standard-4",
        "8vcpu-30gb": "n1-standard-8",
        "16vcpu-60gb": "n1-standard-16",
        "32vcpu-120gb": "n1-standard-32",
        "64vcpu-240gb": "n1-standard-64",
        "96vcpu-360gb": "n1-standard-96",
        "2vcpu-13gb": "n1-highmem-2",
        "4vcpu-26gb": "n1-highmem-4",
        "8vcpu-52gb": "n1-highmem-8",
        "16vcpu-104gb": "n1-highmem-16",
        "32vcpu-208gb": "n1-highmem-32",
        "64vcpu-416gb": "n1-highmem-64",
        "96vcpu-624gb": "n1-highmem-96",
        "2vcpu-1.8gb": "n1-highcpu-2",
        "4vcpu-3.6gb": "n1-highcpu-4",
        "8vcpu-7.2gb": "n1-highcpu-8",
        "16vcpu-14.4gb": "n1-highcpu-16",
        "32vcpu-28.8gb": "n1-highcpu-32",
        "64vcpu-57.6gb": "n1-highcpu-64",
        "96vcpu-86.4gb": "n1-highcpu-96",
        "96vcpu-1.4tb": "n1-megagmem-96",
        "40vcpu-961gb": "n1-ultramem-40",
        "80vcpu-1.88tb": "n1-ultramem-80",
        "160vcpu-3.75tb": "n1-ultramem-160"
    }

    mappings["Amazon Web Services"] = {
        "1vcpu-512mb": "t2.nano",
        "1vcpu-1gb": "t2.micro",
        "1vcpu-2gb": "t2.small",
        "2vcpu-4gb": "t2.medium",
        "2vcpu-8gb": "t2.large",
        "4vcpu-16gb": "t2.xlarge",
        "8vcpu-32gb": "t2.2xlarge",
    }

    if provider in mappings:
        if resource in mappings[provider]:
            return mappings[provider][resource]

    return None