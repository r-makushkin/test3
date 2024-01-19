from transformers import AutoModelForSequenceClassification, AutoTokenizer

model_name = "MonoHime/rubert-base-cased-sentiment-new"
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Сохранение модели и токенизатора локально
model.save_pretrained("models")
tokenizer.save_pretrained("models/local_tokenizer")