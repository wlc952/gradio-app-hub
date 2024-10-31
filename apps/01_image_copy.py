import gradio as gr

STANDALONE = False

def process_image(image):
    return image  # 示例处理：返回未修改的图像

app = gr.Interface(fn=process_image, inputs="image", outputs="image", title="Copy the image you input")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=7860)
    args = parser.parse_args()
    # app = gr.Interface(fn=process_image, inputs="image", outputs="image")
    app.queue().launch(server_port=args.port,inbrowser=True)