from typing import List, Optional
import gradio
from facefusion import state_manager, translator
from facefusion.filesystem import get_file_name, resolve_file_paths
from facefusion.processors.core import get_processors_modules
from facefusion.uis.core import register_ui_component

PROCESSORS_CHECKBOX_GROUP : Optional[gradio.CheckboxGroup] = None

# Mapping for Portuguese Display
PROCESSOR_MAP = {
    'face_swapper': 'Trocador de Rostos',
    'age_modifier': 'Modificador de Idade',
    'background_remover': 'Removedor de Fundo',
    'deep_swapper': 'Trocador Profundo',
    'expression_restorer': 'Restaurador de Expressões',
    'face_debugger': 'Depurador Facial',
    'face_editor': 'Editor de Rostos',
    'face_enhancer': 'Realçador de Rosto',
    'frame_colorizer': 'Colorizador de Quadros',
    'frame_enhancer': 'Aprimorador de Quadros',
    'lip_syncer': 'Sincronizador Labial'
}

# Reverse mapping for internal logic
REVERSE_MAP = {v: k for k, v in PROCESSOR_MAP.items()}

def render() -> None:
    global PROCESSORS_CHECKBOX_GROUP

    # Determine choices and current values in Portuguese
    internal_processors = sort_processors(state_manager.get_item('processors'))
    display_choices = [PROCESSOR_MAP.get(p, p) for p in internal_processors]
    current_values = [PROCESSOR_MAP.get(p, p) for p in state_manager.get_item('processors')]

    PROCESSORS_CHECKBOX_GROUP = gradio.CheckboxGroup(
        label = translator.get('uis.processors_checkbox_group'),
        choices = display_choices,
        value = current_values
    )
    register_ui_component('processors_checkbox_group', PROCESSORS_CHECKBOX_GROUP)

def listen() -> None:
    PROCESSORS_CHECKBOX_GROUP.change(update_processors, inputs = PROCESSORS_CHECKBOX_GROUP, outputs = PROCESSORS_CHECKBOX_GROUP)

def update_processors(display_processors : List[str]) -> gradio.CheckboxGroup:
    # Map back to internal English names
    internal_processors = [REVERSE_MAP.get(p, p) for p in display_processors]
    
    # Original logic using internal names
    for processor_module in get_processors_modules(state_manager.get_item('processors')):
        if hasattr(processor_module, 'clear_inference_pool'):
            processor_module.clear_inference_pool()

    for processor_module in get_processors_modules(internal_processors):
        if not processor_module.pre_check():
            return gradio.CheckboxGroup()

    state_manager.set_item('processors', internal_processors)
    
    # Return translated choices and values
    all_internal = sort_processors(internal_processors)
    all_display = [PROCESSOR_MAP.get(p, p) for p in all_internal]
    current_display = [PROCESSOR_MAP.get(p, p) for p in internal_processors]
    
    return gradio.CheckboxGroup(value = current_display, choices = all_display)

def sort_processors(processors : List[str]) -> List[str]:
    available_processors = [ get_file_name(file_path) for file_path in resolve_file_paths('facefusion/processors/modules') ]
    current_processors = []

    for processor in processors + available_processors:
        if processor in available_processors and processor not in current_processors:
            current_processors.append(processor)

    return current_processors
