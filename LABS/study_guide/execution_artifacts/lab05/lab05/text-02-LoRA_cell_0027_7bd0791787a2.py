# Release the manually adapted model/trainer before loading a fresh baseline.
import gc
globals().pop("trainer", None)
globals().pop("model", None)
gc.collect()
if torch.backends.mps.is_available():
    torch.mps.empty_cache()

set_seed(42)
model_name = "bert-base-uncased"
model = BertForSequenceClassification.from_pretrained(model_name)
tokenizer = BertTokenizer.from_pretrained(model_name)