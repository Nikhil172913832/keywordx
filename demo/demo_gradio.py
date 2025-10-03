from keywordx.pipeline import extract
import gradio as gr

def demo_func(text, keywords):
    keywords_list = [k.strip() for k in keywords.split(",")]
    return extract(text, keywords_list)

demo = gr.Interface(
    fn=demo_func,
    inputs=["text", "text"],
    outputs="json",
    title="KeywordX Demo",
    description="Extract semantic keywords + structured entities"
)

if __name__ == "__main__":
    demo.launch()
