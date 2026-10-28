# Login using a local credential; never store the token in the notebook.
token = get_token()
if token is None:
    raise RuntimeError("Llama 3.2 requires an approved Hugging Face account. Run `hf auth login` locally or set HF_TOKEN, then rerun.")
login(token=token, add_to_git_credential=False)
del token
print("Hugging Face authentication configured.")