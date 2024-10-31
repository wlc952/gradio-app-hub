import gradio as gr

STANDALONE = False

with gr.Blocks() as demo:
  gr.Markdown("## Multi Spaces combination")
  with gr.Tab("Translate to Spanish"):
    gr.load("spaces/gradio/en2es")
  with gr.Tab("Translate to French"):
    gr.load("abidlabs/en2fr", src="spaces")