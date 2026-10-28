from peft import LoraConfig, get_peft_model, PeftModelForSequenceClassification

config = LoraConfig(
    r=8,
    lora_alpha=32, 
    lora_dropout=0.1,
    bias="none",
    # Select the same six linear transformations in each encoder block.
    target_modules=[
        name for name, module in model.named_modules()
        if name.startswith("bert.encoder.layer.") and isinstance(module, nn.Linear)
    ],
)

peft_model = PeftModelForSequenceClassification(model, peft_config=config)