import streamlit as st
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
import requests
from dotenv import load_dotenv
import os

load_dotenv()

COMPUTER_VISION_KEY = os.getenv("COMPUTER_VISION_KEY")
COMPUTER_VISION_ENDPOINT = os.getenv("COMPUTER_VISION_ENDPOINT")

credential = AzureKeyCredential(COMPUTER_VISION_KEY)
client = ImageAnalysisClient(endpoint=COMPUTER_VISION_ENDPOINT, credential=credential)

st.title("Image Analysis with Azure AI Vision")

image_url = st.text_input("분석할 이미지의 URL을 입력하세요:")

if image_url:
    try:
        # URL이 유효한 이미지인지 확인
        response = requests.head(image_url, timeout=10)
        if response.status_code != 200:
            st.error("URL에 접근할 수 없습니다. 유효한 URL인지 확인하세요.")
        elif not response.headers.get('content-type', '').startswith('image/'):
            st.error("입력된 URL은 이미지 파일이 아닙니다. 유효한 이미지 URL을 입력하세요.")
        else:
            # Analyze the image from URL
            result = client.analyze_from_url(
                image_url=image_url,
                visual_features=[VisualFeatures.TAGS, VisualFeatures.OBJECTS]
            )
            
            # Display tags
            if result.tags:
                st.subheader("태그")
                for tag in result.tags.list:
                    st.write(f"{tag.name}: {tag.confidence:.2f}")
            
            # Display objects
            if result.objects:
                st.subheader("객체")
                for obj in result.objects.list:
                    name = obj.tags[0].name
                    conf = obj.tags[0].confidence
                    bbox = obj.bounding_box
                    x, y, w, h = bbox['x'], bbox['y'], bbox['w'], bbox['h']
                    st.write(f"{name}: {conf:.2f} (경계 상자: x={x}, y={y}, w={w}, h={h})")
                    
    except requests.exceptions.RequestException as e:
        st.error(f"URL 요청 중 오류 발생: {str(e)}")
    except Exception as e:
        st.error(f"분석 중 오류 발생: {str(e)}")
        st.info("유효한 이미지 URL을 입력했는지 확인하세요.")