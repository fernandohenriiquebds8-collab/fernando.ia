from typing import Optional

METADATA =\
{
	'name': 'Fernando.IA',
	'description': 'Plataforma oficial de manipulação facial do Fernando',
	'version': '3.5.4',
	'license': 'OpenRAIL-AS',
	'author': 'Fernando',
	'url': 'https://github.com/fernando'
}


def get(key : str) -> Optional[str]:
	return METADATA.get(key)
