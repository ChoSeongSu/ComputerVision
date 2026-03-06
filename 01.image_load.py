from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures # vision 검사 관련
from azure.core.credentials import AzureKeyCredential           #인증 관련
from PIL import Image, ImageDraw, ImageFont

from dotenv import load_dotenv
import os

load_dotenv()

COMPUTER_VISION_KEY = os.getenv("COMPUTER_VISION_KEY")
COMPUTER_VISION_ENDPOINT = os.getenv("COMPUTER_VISION_ENDPOINT")

image = Image.open("/workspaces/ComputerVision/catdog.PNG")
image.show()

credential = AzureKeyCredential(COMPUTER_VISION_KEY)
client = ImageAnalysisClient(endpoint=COMPUTER_VISION_ENDPOINT, credential= credential)

def get_image_info():
    image_path = "/workspaces/ComputerVision/catdog.PNG"

    with open(image_path, "rb") as image_file: #read binary
        image_data = image_file.read()

    result = client.analyze(
        image_data=image_data,
        visual_features=[VisualFeatures.TAGS,
                         VisualFeatures.OBJECTS]
    )

    #tags를 출력 하는 부문
    if result.tags is not None:
        print("Tags: ")
        for tag in result.tags.list:
            print(f"    {tag.name} ({tag.confidence:.2f})")

    # # caption을 출력하는 부분
    # if result.caption is not None:
    #     print("Caption: ")
    #     print(f"    {result.caption.text} ({result.caption.confidence:.2f})")

    #object를 출력하는 부분
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    if result.objects is not None:
        print("Objects: ")
        for obj in result.objects.list:
            print(f"    {obj.tags[0].name} ({obj.tags[0].confidence:.2f}) - Bounding Box: {obj.bounding_box}")

            x,y,w,h = obj.bounding_box['x'],obj.bounding_box['y'],obj.bounding_box['w'],obj.bounding_box['h'],
            draw.rectangle(((x,y),(x+w,y+h)), outline="red", width=2)
            draw.text((x,y), obj.tags[0].name, fill="red")

        image.save("output.png")

get_image_info()