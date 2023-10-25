import os
# Configure SOMEF, see https://github.com/KnowledgeCaptureAndDiscovery/somef#configure
os.system("pip install -r requirements.txt")
os.system("python -m nltk.downloader wordnet")
os.system("python -m nltk.downloader omw-1.4")
os.system("python -m nltk.downloader punkt")
os.system("python -m nltk.downloader stopwords")
os.system("somef configure -a")
