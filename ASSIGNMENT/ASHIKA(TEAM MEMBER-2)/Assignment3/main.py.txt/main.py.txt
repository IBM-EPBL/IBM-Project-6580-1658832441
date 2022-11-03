from flask import *
import ibm_boto3
from ibm_botocore.client import Config, ClientError

COS_ENDPOINT = "https://s3.jp-tok.cloud-object-storage.appdomain.cloud"
COS_API_KEY_ID = "izhab7-4xLr1kfqFVD7aOkORdBRKueFWpXmktu63ZXbG"
COS_INSTANCE_CRN = "crn:v1:bluemix:public:iam-identity::a/ef3a8fe479784ab6becbe96a6c30a243::serviceid:ServiceId-79c18bfc-c4fc-41e1-bfff-b1322e6321c7"

cos = ibm_boto3.resource("s3",
                         ibm_api_key_id=COS_API_KEY_ID,
                         ibm_service_instance_id=COS_INSTANCE_CRN,
                         config=Config(signature_version="oauth"),
                         endpoint_url=COS_ENDPOINT
                         )

app = Flask(__name__)


def delete_item(bucket_name, object_name):
    try:
        cos.delete_object(Bucket=bucket_name, Key=object_name)
        print("Item: {0} deleted!\n".format(object_name))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to delete object: {0}".format(e))


def multi_part_upload(bucket_name, item_name, file_path):
    try:
        print("Starting file transfer for {0} to bucket: {1}\n".format(item_name, bucket_name))

        part_size = 1024 * 1024 * 5

        file_threshold = 1024 * 1024 * 15

        transfer_config = ibm_boto3.s3.transfer.TransferConfig(
            multipart_threshold=file_threshold,
            multipart_chunksize=part_size
        )

        with open(file_path, "rb") as file_data:
            cos.Object(bucket_name, item_name).upload_fileobj(
                Fileobj=file_data,
                Config=transfer_config
            )

        print("Transfer for {0} Complete!\n".format(item_name))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to complete multi-part upload: {0}".format(e))


@app.route('/uploader', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        bucket = request.form['bucket']
        name_file = request.form['filename']
        f = request.files['file']
        multi_part_upload(bucket, name_file, f.filename)
        return 'file uploaded successfully'

    if request.method == 'GET':
        return render_template('Upload.html')


@app.route('/deletefile', methods=['GET', 'POST'])
def deletefile():
    if request.method == 'POST':
        bucket = request.form['bucket']
        name_file = request.form['filename']

        delete_item(bucket, name_file)
        return 'file deleted successfully'

    if request.method == 'GET':
        return render_template('delete.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)