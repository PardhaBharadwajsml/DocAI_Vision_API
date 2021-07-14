from google.cloud import vision,storage
import io 
import re
bucket_name = "gcp-training-gcs-bucket"
storage_client = storage.Client()
def detect_text(uri):
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri
    response = client.text_detection(image=image)
    texts = response.text_annotations

    bucket = storage_client.bucket(bucket_name)
    
    # blob.upload_from_string(str(texts))
    print('Texts:')

    fullText = ""
    for text in texts:
        #print('\n"{}"'.format(text.description))
        fullText = fullText+text.description
    print(fullText)
    blob = bucket.blob('visionapi/raw_text_output.txt')
    blob.upload_from_string(str(fullText))
    invoiceNumber = re.search('INVOICE\n*\s*#\s*(.*)\s*\n*From', fullText)
    if invoiceNumber:
        invoiceNumber = invoiceNumber.group(1)
        print('invoice number:',invoiceNumber)
    else:
        invoiceNumber = "not present"
    blob = bucket.blob('visionapi/output_invoice.txt')
    blob.upload_from_string(str(invoiceNumber))
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

path = "gs://gcp-training-gcs-bucket/visionapi/67546756-1.jpg"
detect_text(path)