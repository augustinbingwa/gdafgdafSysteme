from django.apps import AppConfig

class ModParametrageConfig(AppConfig):
	name = 'mod_parametrage'

	def ready(self):
		from mod_helpers.hlp_global_variables import GlobalVariablesHelpers

		GlobalVariablesHelpers.save_global_variables()

		pass # startup code here.