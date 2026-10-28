# Dynamic padding shortens each one-example physical microbatch to its content.
# With microbatch=1, length grouping cannot further reduce training padding; its
# measurable benefit is the six-example logical-batch comparison above.
dynamic_run = train_padding_variant("dynamic-padding", "dynamic")