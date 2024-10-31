import gradio as gr

STANDALONE = False

def process_text(text):
    return text  # 示例处理：返回未修改的文本

app = gr.Interface(fn=process_text, inputs="text", outputs="text", title="Copy the text you input")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=7860)
    args = parser.parse_args()
    app = gr.Interface(fn=process_text, inputs="text", outputs="text")
    app.queue().launch(server_port=args.port, inbrowser=True)