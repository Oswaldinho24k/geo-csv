import os
import string
import secrets
import unicodedata
import uuid
import boto3
import psutil


alphabet = string.ascii_letters + string.digits


def cryptosecure_string_generator(size=12):
    """ Generate a cryptosecure string, of default size 12.
    """
    return ''.join(secrets.choice(alphabet) for i in range(size))


def normalize_string(unormalized_string):
    """
    Receives a string and returns it's value without any special characters
    """
    return unicodedata.normalize('NFKD', unormalized_string).encode('ascii', 'ignore')


def is_production():
    """
    Check wether the current environment is production or not
    """
    if os.environ['DJANGO_SETTINGS_MODULE'] == 'iupick.settings.production':
        return True
    else:
        return False


def get_environment():
    """
    Check wether the current environment is production or not
    """
    if os.environ['DJANGO_SETTINGS_MODULE'] == 'iupick.settings.production':
        return 'Production'
    elif os.environ['DJANGO_SETTINGS_MODULE'] == 'iupick.settings.development':
        return 'Development'
    elif os.environ['DJANGO_SETTINGS_MODULE'] == 'iupick.settings.sandbox':
        return 'Sandbox'
    else:
        return 'CI'


def get_hardware_information():
    server = {}
    cpu_percent = psutil.cpu_percent(interval=1, percpu=False)
    server['cpu_percent'] = cpu_percent
    ram_percent = psutil.virtual_memory()[2]
    server['ram_percent'] = ram_percent
    return server


def store_pdf(binary_pdf_data):
    """
    Receives the binary data for a new pdf file
    Returns its URI
    """
    binary_pdf_data
    label_file_name = str(uuid.uuid4()) + '.pdf'
    label_file_path = '/tmp/' + label_file_name

    with open(label_file_path, 'wb+') as label:
        label.write(binary_pdf_data)

    s3 = boto3.client('s3',
                      aws_access_key_id=os.environ['AWS_KEY'],
                      aws_secret_access_key=os.environ['AWS_SECRET_KEY'])
    bucket_name = 'iupick-guias'
    s3.upload_file(label_file_path, bucket_name, label_file_name)
    os.remove(label_file_path)

    s3_base_url = 'https://s3-us-west-1.amazonaws.com/iupick-guias/'
    file_uri = s3_base_url + label_file_name

    return file_uri
