for layer in model.bert.encoder.layer:
    layer.attention.self.query = LoRA(layer.attention.self.query)
    layer.attention.self.key = LoRA(layer.attention.self.key)
    layer.attention.self.value = LoRA(layer.attention.self.value)
    layer.attention.output.dense = LoRA(layer.attention.output.dense)
    layer.intermediate.dense = LoRA(layer.intermediate.dense)
    layer.output.dense = LoRA(layer.output.dense)