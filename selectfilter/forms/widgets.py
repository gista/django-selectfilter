# -*- coding: utf-8 -*-
import operator

from django.conf import settings
from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from selectfilter import utils


def _renderFilter(js_method_name, element_id, model, lookup_list, 
	select_related):
	"""Return the html output of a filter link."""
	label, lookup_dict = lookup_list
	script = "selectfilter.%s('%s', '%s', '%s', '%s', '%s')" % (
		js_method_name,
		element_id,
		model._meta.app_label, 
		model._meta.object_name, 
		utils.lookupToString(lookup_dict),
		select_related)
	return '<option value="%s">%s</option> '% (script, label)

class FilteredSelectMultiple(forms.SelectMultiple):
			
	def render(self, name, value, attrs=None, choices=()):
		self._element_id = attrs['id']
		# choices links
		# if there is only one choice, then nothing will be rendered
		lookups_output = ""
		lookups = utils.getLookups(self.lookups)
		if len(lookups) > 1:
			js_method_name = "getManyToManyJSON"
			lookups_output = "\n".join(
				_renderFilter(js_method_name, self._element_id, 
					self.model, i, self.select_related) 
				for i in lookups)
			lookups_output = '<select onChange="eval(this.value)">%s</select>' % lookups_output
		# normal widget output from the anchestor
		self.choices = self._getAllChoices(value)				
		parent_output = super(FilteredSelectMultiple, self
			).render(name, value, attrs, choices)
		
		# create the output including the django admin's Javascript code that
		# mutates the select widget into a selectfilter one
		# this assumes that /admin/jsi18n/, core.js, SelectBox.js and
		# SelectFilter2.js are loaded from the page
		verbose_name = self.model._meta.verbose_name_plural.replace('"', '\\"')
		
		output = u"""
			<div>
				%s
			</div>
			%s
			<script type="text/javascript">
				(function($) {
					$(document).ready(function(){
						SelectFilter.init("id_%s", "%s", 0, "%s");
					});
				})(django.jQuery);
			</script>
		""" % (lookups_output, parent_output, name, 
			verbose_name, settings.ADMIN_MEDIA_PREFIX)
		
		return mark_safe(output)
		
	def _getAllChoices(self, value):
		value = value or []
		choices = list(self.choices)
		# convert to unicode for safe comparisong during a ValidationError
		choices_keys = [unicode(i[0]) for i in choices]
		for i in value:
			if not unicode(i) in choices_keys:
				obj = utils.getObject(self.model, {"pk": i}, self.select_related)
				choices.append((i, unicode(obj)))
		choices.sort(key=operator.itemgetter(1))
		return choices

