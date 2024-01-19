#!/usr/bin/env bash
sudo apt update
apt-get update && apt-cache search python3.10
sudo apt update pip
pip install streamlit telethone asyncio pandas torch transformers nltk wordcloud
cd models
mkdir "local_tokenizer"
python3 get_models.py