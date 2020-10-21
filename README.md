# Requirements

The script requires python3 and uses selenium with a chrome to function.

## Selenium

Install selenium:

`pip3 install selenium`

Following the [installation instructions](https://selenium-python.readthedocs.io/installation.html#drivers) of selenium, make sure to also install chrome and the [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads).

> Don't forget to add chromedriver to the PATH

# Installation

Clone the repo.
  
`git clone https://github.com/pedrus16/visa.git ~/visa`

To send alerts using emails you will need to edit and run the files in the `email/` directory.
For twitter alerts, the scripts are in the `twitter/` directory.

## Configuration

Edit the `config.py` file in the directory corresponding to your choice (`email/` or `twitter/`) and set the `directory_path` variable. This is where the logs and temporary files will be created and stored.

You can use the script's folder as a path for example: 
```python
directory_path = '~/visa/twitter/
```

After running the script once, a `visa.log` and other useful files for the script will be created in this directory.

If you want to send emails jump to [Email Configuration](https://github.com/pedrus16/visa/new/main?readme=1#email-configuration), otherwise continue reading.

### Twitter configuration

You will need to create a Twitter app on the [developper dashboard](https://developer.twitter.com/en/portal/dashboard) and generate the API keys.

Edit the `twitter/config.py` file and add your keys:

```python
twitter_keys = {
    'api_key': '123412341234',
    'api_key_secret': '123412341234',
    'access_token': '123412341234',
    'access_token_secret': '123412341234'
}
```

### Email configuration

You will need a Gmail account with less secured apps authorized. I recommend creating a dedicated account because it might put your main account at risk. See [Authorize less secured apps](https://myaccount.google.com/lesssecureapps).

Edit the `email/config.py` file and enter your gmail account credentials :

```python
sender_email = 'my-email@gmail.com'
sender_password = 'password'
```

Also add the email addresses of the people you want to send the alerts to:
```python
# List of recipients emails
mail_repicients = [
  'john.smith@live.fr',
  'alice.doe@yahoo.com',
]
```

### Appointment configuration

To tell the script what prefectures and appointments to check you need to edit the `appointments.py` file.
```python
appointments = [
    {
        # URL of the appointment page (the one with the checkbox to accept the conditions)
        'url': 'http://www.hauts-de-seine.gouv.fr/booking/create/12069/0',

        'desk_ids': None,

        # A unique name without spaces or special characters. this is used for naming temporary files
        'unique_name': 'nanterre_renouv_privee',

        # This is used for the tweet message
        'prefecture_name': 'NANTERRE',
        'appointment_name': 'Renouvellement de titre de séjour "vie privée et familiale"',
    },
    # Add more as needed
]
```

Once this is done, check if your script works by running:

`python3 ~/visa/email/visa.py` for emails

or

`python3 ~/visa/twitter/visa.py` for Twitter

If no error appears and logs are added in the `visa.log` file, you can proceed to the next step.

## Run as a service

To run the script continuously and check for appointments 24/7 you can use systemd to run it as a service.

Copy `visa.service` to `/etc/systemd/system/` and edit the file:

Modify the paths on line 5 to match python and your script locations

```
ExecStart=/usr/bin/python3.7 ~visa/twitter/visa.py
```

Also change the user and group names on lines 8-9 to match yours:
```
User=user
Group=user
```

# Usage

Enable the service with (this will start the service on boot)

`systemctl enable visa.service`

Start the service manually with:

`systemctl start visa.service`

And you can stop the service by running:

`systemctl stop visa.service`

# Help & Contact

If you have any issue with the installation or for any other reason you can contact me on twitter [@NanterreRDV](https://twitter.com/NanterreRdv) (FR or EN)
