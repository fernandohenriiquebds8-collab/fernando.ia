from typing import Optional
import gradio
import os
import shutil
import hashlib
from facefusion import state_manager, process_manager, logger
from facefusion.filesystem import is_image, is_video
from facefusion.processors.core import get_processors_modules
from facefusion.core import conditional_process

def render() -> None:
    with gradio.Column():
        with gradio.Row():
            gradio.HTML('''
                <div style="flex-grow: 1; text-align: center; padding: 20px; background: rgba(128, 0, 128, 0.1); border-radius: 15px; border: 1px solid rgba(128, 0, 128, 0.3); margin-bottom: 25px;">
                    <h2 style="margin: 0; color: #d8b4fe; font-family: 'Outfit', sans-serif;">✨ GenSpark AI Workspace</h2>
                    <p style="color: #a78bfa; margin: 5px 0 0 0;">Editor de IA Conectado: Edição Técnica e Facial</p>
                </div>
            ''')
        
        with gradio.Row():
            with gradio.Column(scale=2):
                upload_img = gradio.Image(
                    label='📥 1. Upload da Imagem Original',
                    type='filepath',
                    elem_id='genspark_upload',
                    sources=['upload']
                )
                
                with gradio.Row():
                    prompt = gradio.Textbox(
                        label='⌨️ 2. Instruções para a IA (Texto)',
                        placeholder='Ex: "Remova o fundo", "Melhore o rosto"...',
                        lines=3,
                        scale=4
                    )
                    help_btn = gradio.Button('❓', size='sm', scale=1)
                
                help_content = gradio.HTML('''
                    <div style="padding: 15px; background: rgba(139, 92, 246, 0.1); border: 1px dashed #8b5cf6; border-radius: 10px; margin-top: 10px; font-size: 0.85em;">
                        <b style="color: #d8b4fe;">🚀 Comandos que você pode usar:</b><br>
                        • <b>Remover Fundo:</b> "Remova o fundo", "Tire o fundo"<br>
                        • <b>Melhorar Rosto:</b> "Melhore o rosto", "Aumente a nitidez", "Limpe a pele"<br>
                        • <b>Idade:</b> "Mude a idade para velho", "Deixe mais novo"<br>
                        • <b>Expressão:</b> "Adicione um sorriso", "Melhore o olhar"<br>
                        <br><i style="color: #a78bfa;">Nota: Mudanças generativas (como trocar roupas) ainda não são suportadas.</i>
                    </div>
                ''', visible=False)
                
                with gradio.Row():
                    style = gradio.Dropdown(
                        label='🎨 Estilo Predominante',
                        choices=['Realista', 'Cinematográfico', 'Vetor', 'Especial'],
                        value='Realista'
                    )
                
                submit_btn = gradio.Button('🚀 Iniciar Edição Mágica', variant='primary')
                
                log_box = gradio.HTML(visible=False)

            with gradio.Column(scale=3):
                editor_output = gradio.Image(
                    label='🖼️ Resultado Processado pela IA',
                    type='filepath',
                    interactive=False
                )
                
                download_file = gradio.File(
                    label='📥 Link Direto para Download',
                    visible=False
                )

        def toggle_help():
            return gradio.update(visible=True)

        help_btn.click(fn=toggle_help, outputs=help_content)

        def proceed_edit(img_path, text):
            if not img_path:
                return None, gradio.update(visible=False), gradio.update(visible=False)
            
            text_orig = text
            text = text.lower()
            active_processors = []
            
            # Mapping
            if any(word in text for word in ['fundo', 'background', 'remover']):
                active_processors.append('background_remover')
            if any(word in text for word in ['rosto', 'melhore', 'clareza', 'enhance', 'nitidez']):
                active_processors.append('face_enhancer')
            if any(word in text for word in ['idade', 'velho', 'novo', 'age']):
                active_processors.append('age_modifier')
                state_manager.set_item('age_modifier_direction', 50 if 'velho' in text else -50)
            if any(word in text for word in ['expressão', 'sorriso', 'olho', 'smile']):
                active_processors.append('expression_restorer')
            
            if not active_processors:
                msg = "<div style='color: #ef4444; padding: 10px; background: rgba(239, 68, 68, 0.1); border-radius: 5px;'>⚠️ Comando não suportado. Clique no botão de ajuda (?) para ver exemplos.</div>"
                return None, gradio.update(visible=False), gradio.update(value=msg, visible=True)

            output_dir = state_manager.get_item('output_path')
            file_hash = hashlib.sha1(str(img_path + text_orig).encode()).hexdigest()[:8]
            final_output_path = os.path.join(output_dir, f"editor_{file_hash}.jpg")
            
            try:
                old_processors = state_manager.get_item('processors')
                old_target = state_manager.get_item('target_path')
                old_output = state_manager.get_item('output_path')
                
                state_manager.set_item('processors', active_processors)
                state_manager.set_item('target_path', img_path)
                state_manager.set_item('output_path', final_output_path)
                
                conditional_process()
                
                state_manager.set_item('processors', old_processors)
                state_manager.set_item('target_path', old_target)
                state_manager.set_item('output_path', old_output)
                
                msg = "<div style='color: #10b981; padding: 10px; background: rgba(16, 185, 129, 0.1); border-radius: 5px;'>✅ Edição concluída com sucesso!</div>"
                return final_output_path, gradio.update(value=final_output_path, visible=True), gradio.update(value=msg, visible=True)
            except Exception as e:
                msg = f"<div style='color: #ef4444; padding: 10px; background: rgba(239, 68, 68, 0.1); border-radius: 5px;'>❌ Erro ao processar: {str(e)}</div>"
                return None, gradio.update(visible=False), gradio.update(value=msg, visible=True)

        submit_btn.click(
            fn=proceed_edit,
            inputs=[upload_img, prompt],
            outputs=[editor_output, download_file, log_box]
        )

def listen() -> None:
    pass
