import gradio as gr

DESCRIPTION = "根据文本内容，生成情绪预测的标签及概率"
STANDALONE = True

gr.Markdown(f"## {DESCRIPTION}", elem_id="welcome_message")

if __name__ == '__main__':
    import argparse
    from transformers import pipeline
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=7860)
    args = parser.parse_args()
    app = gr.Interface.from_pipeline(pipeline("text-classification", model="uer/roberta-base-finetuned-dianping-chinese"), title="Text Classification", description=DESCRIPTION)
    app.queue().launch(server_port=args.port,inbrowser=True)