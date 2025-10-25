from keywordx.pipeline import extract
import gradio as gr

def demo_func(text, keywords):
    keywords_list = [k.strip() for k in keywords.split(",")]
    result = extract(text, keywords_list)
    entities = result.get("entities", [])
    matches = result.get("semantic_matches", [])

    entity_text = "\n".join([f"• {e['text']} ({e['type']})" for e in entities]) or "No entities found"
    match_text = "\n".join([f"• {m['keyword']} → {m['match']} (score: {m['score']:.2f})" for m in matches]) or "No matches found"
    
    return entity_text, match_text

with gr.Blocks(title="KeywordX Dashboard") as demo:
    gr.Markdown(
        """
        # 🧠 KeywordX Dashboard  
        Extract **semantic keywords** and **entities** from your text using NLP.
        """
    )
    
    with gr.Row():
        with gr.Column(scale=2):
            text_input = gr.Textbox(label="Enter your text", lines=5, placeholder="Type a sentence...")
            keywords_input = gr.Textbox(label="Enter keywords (comma-separated)", placeholder="e.g. meeting, date, time, place")
            submit_btn = gr.Button("🔍 Extract")

        with gr.Column(scale=1):
            entities_output = gr.Textbox(label="Named Entities", lines=6)
            matches_output = gr.Textbox(label="Semantic Matches", lines=6)

    submit_btn.click(demo_func, inputs=[text_input, keywords_input], outputs=[entities_output, matches_output])

demo.launch()
