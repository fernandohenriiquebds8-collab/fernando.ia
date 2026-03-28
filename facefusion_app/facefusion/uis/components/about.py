import random
import base64
import os
from typing import Optional

import gradio

from facefusion import metadata, translator

METADATA_BUTTON : Optional[gradio.Button] = None
ACTION_BUTTON : Optional[gradio.Button] = None


def _get_logo_b64() -> str:
	logo_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'logo.png')
	try:
		with open(logo_path, 'rb') as f:
			return base64.b64encode(f.read()).decode()
	except Exception:
		return ''


def render() -> None:
	global METADATA_BUTTON
	global ACTION_BUTTON

	action = random.choice(
	[
		{
			'text': 'Apoiar o Projeto',
			'url': 'https://github.com'
		},
		{
			'text': 'Seja Membro',
			'url': 'https://github.com'
		},
		{
			'text': 'Entre na Comunidade',
			'url': 'https://github.com'
		}
	])

	b64 = _get_logo_b64()
	img_tag = f'<img src="data:image/png;base64,{b64}" style="width:60px;height:60px;border-radius:50%;border:2px solid #a855f7;object-fit:cover;" />' if b64 else '<span style="font-size:2.5em;">🧠</span>'

	gradio.HTML(f'''
		<div style="
			display: flex;
			align-items: center;
			gap: 16px;
			padding: 16px 22px;
			background: linear-gradient(135deg, rgba(88,28,135,0.55) 0%, rgba(20,5,50,0.9) 100%);
			border-radius: 18px;
			border: 1px solid rgba(168,85,247,0.45);
			margin-bottom: 10px;
			box-shadow: 0 4px 40px rgba(128,0,255,0.2);
		">
			{img_tag}
			<div>
				<div style="font-size:1.5em;font-weight:900;color:#f0e6ff;font-family:'Outfit',sans-serif;letter-spacing:1.5px;text-shadow:0 0 12px #a855f7;">
					🔬 Fernando.IA
				</div>
				<div style="font-size:0.78em;color:#a855f7;margin-top:3px;font-style:italic;">
					Plataforma de IA Avançada · v3.5.4
				</div>
			</div>
		</div>
	''')

	ACTION_BUTTON = gradio.Button(
		value = action.get('text'),
		link = action.get('url'),
		size = 'sm'
	)
