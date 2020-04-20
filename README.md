# GlobeSpinner
ChatOps bot for fully automated Cloud Infrastructure deployments using Terraform, the popular IaC (Infrastructure as Code) tool.

## Features
 - Deploy Cloud Infrastructure on the fly, using a simple chat interface. Sessions are isolated and stored securely in the Zulip bot storage (Check [here](https://zulipchat.com/api/writing-bots#bot_handlerstorage) for more information).
 - Natural Language Processing: Understands natural human language.
 - Abstract away complex terms involved with deploying infra, asks simple questions about the configuration.
 - Completely automated deployments using [Terraform](https://terraform.io). Rolls back all changes if errors occured. Verbose and crystal-clear error messages.
 - Supports over 100 cloud providers! Just add a terraform config and you're good to go. Sample configs for 3 major providers are available in the ```configs``` directory.

## Running the bot
 - ```git clone https://github.com/zulip/python-zulip-api.git``` - clone the python-zulip-api repository.
 - ```cd python-zulip-api``` - navigate into your cloned repository.
 - The output of provision will end with a command of the form ```source .../activate```; run that command to enter the new virtualenv.
 - ```git clone https://github.com/ATechnoHazard/globespinner.git ./zulip_bots/zulip_bots/bots/globespinner``` - Clone this bot.
 - Obtain a valid ```zuliprc``` by following the instructions [here](https://zulipchat.com/api/running-bots). Place it in the dir you cloned the bot to.
 - ```cd zulip_bots/zulip_bots/bots/globespinner``` - Navigate to the bot directory.
 - ```pip install -r requirements.txt``` - Install dependencies.
 - Create a DialogFlow agent by importing the ```globespinner.zip``` file at https://dialogflow.cloud.google.com.
 - Connect a service account to the DialogFlow agent, and download a json file with the service account credentials from https://console.cloud.google.com.
 - Set the ```GOOGLE_APPLICATION_CREDENTIALS``` environment variable by assigning it the absolute path to the json file you downloaded.
 - Add the necessary credentials to the Terraform config files, which can be found in ```./configs/<provider>```
 - ```zulip-run-bot globespinner --config-file ./zuliprc``` - Start up the bot.
 - Interact with the bot in whichever workspace you added it in.

## Why isn't a deployed instance available?
Deployed instances have access to extremely sensitive keys that allow access to my AWS, GCP and DigitalOcean accounts. I don't want anyone abusing the usage of the bot and racking up millions in fees.

You can avoid this issue by restricting your workspace.

