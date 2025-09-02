import gradio as gr
from deep_translator import GoogleTranslator
from gtts import gTTS
import tempfile
import os
import atexit

# Supported languages
languages = {
    'English': 'en',
    'Spanish': 'es',
    'Arabic' : 'ar',
    'French' : 'fr',
    'German': 'de',
    'Chinese (Simplified)': 'zh-CN',
    'Japanese': 'ja',
    'Russian': 'ru',
    'Italian': 'it',
    'Portuguese': 'pt',
    'Hindi': 'hi',
}

# Keep track of temporary files to delete on exit
tmp_files = []

def translate_text(text, source_lang, target_lang):
    if not text.strip():
        return "Please enter text to translate.", None

    try:
        if source_lang == "Auto":
            translated_text = GoogleTranslator(source='auto', target=languages[target_lang]).translate(text)
        else:
            translated_text = GoogleTranslator(source=languages[source_lang], target=languages[target_lang]).translate(text)
    except Exception as e:
        return f"Translation error: {str(e)}", None

    # Text-to-Speech
    try:
        tts = gTTS(translated_text, lang=languages[target_lang])
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(tmp_file.name)
        tmp_files.append(tmp_file.name)
        return translated_text, tmp_file.name
    except Exception:
        return translated_text, None

# Ensure temporary files are cleaned up on exit
atexit.register(lambda: [os.unlink(f) for f in tmp_files if os.path.exists(f)])

# --- Gradio UI ---
with gr.Blocks() as demo:
    gr.Markdown("# 🌐 Language Translation Tool (Google Translate)")

    with gr.Row():
        source_lang = gr.Dropdown(choices=["Auto"] + list(languages.keys()), value="Auto", label="Source Language")
        target_lang = gr.Dropdown(choices=list(languages.keys()), value="French", label="Target Language")

    input_text = gr.Textbox(lines=6, placeholder="Enter text here...", label="Input Text")
    translate_btn = gr.Button("Translate")
    output_text = gr.Textbox(lines=6, label="Translated Text")
    audio_output = gr.Audio(label="Text-to-Speech", type="filepath")

    translate_btn.click(
        fn=translate_text,
        inputs=[input_text, source_lang, target_lang],
        outputs=[output_text, audio_output]
    )

demo.launch()