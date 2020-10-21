# visa
visa crawler script

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

// TODO
