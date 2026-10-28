# Both variants start from the same public checkpoint and use identical data,
# seeds, optimizer, accumulation, and a matched 12-update training window.
fixed_run = train_padding_variant("fixed-padding", "fixed")