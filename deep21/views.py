import sys
import os
import logging
import requests
import shutil
import pyimgur
import botocore
import hashids
import yaml

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework.decorators import api_view
from two1.bitserv.django import payment

from deep21 import settings
from deep21 import aws
from deep21.models import Request

hasher = hashids.Hashids(salt=settings.HASHIDS_SALT, min_length=5)

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def filepaths(token):
    names = {}

    for fname in [settings.CONTENT_SUFFIX, settings.STYLE_SUFFIX, settings.OUTPUT_SUFFIX]:
        names[fname] = '{}{}-{}.jpg'.format(settings.TMP_DIR, token, fname)

    return names


def fetch_files(data, filepath_dict):
    '''
        Fetch the files given by urls in data['style'] and data['content']
        and save them to the corresponding file paths given in filepath_dict.
    '''
    logger.info('Fetching remote files')
    for key, filepath in filepath_dict.items():
        if key != settings.OUTPUT_SUFFIX:
            file_url = data[key]
            logger.info('Fetching remote {} file: {}'.format(key, file_url))
            response = requests.get(file_url, stream=True)

            if response.status_code == 200:
                with open(filepath, 'wb') as outfile:
                    response.raw.decode_content = True
                    shutil.copyfileobj(response.raw, outfile)
            else:
                raise FileNotFoundError('Received 404 when fetching {}'.format(file_url))


def validate_buy_params(data):
    validated_data = {}

    try:
        content = data['content']
        if not content.endswith('.jpg'):
            raise ValidationError('Content image must be a url to a .jpg file')
        validated_data['content'] = content

        style = data['style']
        if not style.endswith('.jpg'):
            raise ValidationError('Content image must be a url to a .jpg file')
        validated_data['style'] = style
    except KeyError as e:
        raise ValidationError("'{}' must be specified as a POST parameter".format(e.args[0]))

    if aws.num_running_instances() >= settings.EC2_MAX_NUM_INSTANCES:
        raise ValidationError('All EC2 instances are busy. Try again in 20 minutes.')

    return validated_data


def _execute_buy(data):
    request = Request.objects.create()

    request.token = hasher.encode(request.id)
    filepath_dict = filepaths(request.token)

    request.output_filepath = filepath_dict[settings.OUTPUT_SUFFIX]
    request.output_s3_filename = os.path.split(request.output_filepath)[1]
    request.save()

    try:
        fetch_files(data, filepath_dict)
    except FileNotFoundError as e:
        return JsonResponse({"error": e.message}, status=404)

    try:
        aws.launch(filepath_dict, data)
    except Exception as e:
        return JsonResponse({"error": "Error with AWS: {}".format(str(e))}, status=500)

    return JsonResponse({"token": request.token}, status=200)


@api_view(['POST'])
@payment.required(settings.BUY_PRICE)
def buy(request):
    try:
        data = validate_buy_params(request.data)
    except ValidationError as error:
        return JsonResponse({"error": error.message}, status=400)

    return _execute_buy(data)


def try_download_output(request):
    s3_filename = request.output_s3_filename
    output_filepath = request.output_filepath
    aws.download_from_s3(output_filepath, s3_filename)


def validate_redeem_params(request):
    try:
        token = request.GET['token']
    except KeyError:
        raise ValidationError({
            "error_message":
            "'token' must be specified as a GET parameter"
        })

    return token


def _redeem(token):
    try:
        request = Request.objects.get(token=token)
        if request.redeemed:
            raise ValueError()

        try_download_output(request)
    except botocore.exceptions.ClientError as e:
        logger.error('Download from S3 failed with error: {}'.format(str(e)))
        return JsonResponse({'status': 'working', 'message': 'Not yet finished.'}, status=202)
    except ObjectDoesNotExist:
        logger.error('User requested token {} that does not exist'.format(token))
        return JsonResponse({'error': 'Invalid or redeemed token.'}, status=400)
    except ValueError:
        logger.error('User requested token {} that was already redeemed'.format(token))
        return JsonResponse({'error': 'Invalid or redeemed token.'}, status=400)

    imgur = pyimgur.Imgur(settings.IMGUR_CLIENT_ID)
    uploaded_image = imgur.upload_image(request.output_filepath, title='Style transfer output {}'.format(token))
    url = uploaded_image.link

    request.redeemed = True
    request.save()

    return JsonResponse({"status": "finished", "url": url, "message": "Thanks!"}, status=200)


@api_view(['GET'])
def redeem(request):
    try:
        token = validate_redeem_params(request)
    except ValidationError as error:
        return JsonResponse({"error": error.message}, status=400)

    return _redeem(token)


@api_view(['GET'])
def manifest(request):
    with open(settings.BASE_DIR + "/deep21/manifest.yaml", 'r') as infile:
        return JsonResponse(yaml.load(infile), status=200)
