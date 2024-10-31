import gradio as gr

DESCRIPTION = "YOLO11n 目标检测"
STANDALONE = True

gr.Markdown(f"## {DESCRIPTION}",  elem_id="welcome_message")

if __name__ == '__main__':
    import argparse
    from ultralytics import YOLO
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=7860)
    args = parser.parse_args()

    model = YOLO("../yolo11n.pt")

    def predict_image(img, conf_threshold, iou_threshold):
        results = model.predict(
            source=img,
            conf=conf_threshold,
            iou=iou_threshold,
            show_labels=True,
            show_conf=True,
        )
        return results[0].plot() if results else None

    app = gr.Interface(
        fn=predict_image,
        inputs=[
            gr.Image(type="pil", label="Upload Image"),
            gr.Slider(minimum=0, maximum=1, value=0.25, label="Confidence threshold"),
            gr.Slider(minimum=0, maximum=1, value=0.45, label="IoU threshold"),
        ],
        outputs=gr.Image(type="pil", label="Result"),
        title="Ultralytics Gradio YOLO11",
        description="Upload images for YOLO11 object detection.",
        theme="huggingface",
    )
    app.queue().launch(server_port=args.port,inbrowser=True)