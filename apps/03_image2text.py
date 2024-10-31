import gradio as gr

DESCRIPTION = "根据图像内容生成文本描述"
STANDALONE = True

gr.Markdown(f"## {DESCRIPTION}",  elem_id="welcome_message")

if __name__ == '__main__':
    import argparse
    from transformers import pipeline
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=7860)
    args = parser.parse_args()
    app = gr.Interface.from_pipeline(pipeline("image-to-text"), title="Image to Text", description=DESCRIPTION)
    app.queue().launch(server_port=args.port,inbrowser=True)