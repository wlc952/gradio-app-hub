import gradio as gr

STANDALONE = False

app = gr.load("stabilityai/stable-diffusion-3.5-large", src="models", token="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")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=7860)
    args = parser.parse_args()
    app.queue().launch(server_port=args.port, inbrowser=True)
