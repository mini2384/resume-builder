import os
import sys

# 프로젝트 루트 경로를 sys.path에 추가하여 app 모듈 import 지원
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import app
