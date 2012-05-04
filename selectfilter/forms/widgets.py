# -*- coding: utf-8 -*-
import operator

from django.conf import settings
from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from selectfilter import utils

class SelectBoxFilter(object):

	def renderFilter(self, js_method_name, element_id, model, lookups, select_related, default_index=0):
		if len(lookups) <= 1:
			return ""
		def renderElement(index, lookup):
			label, lookup_dict = lookup
			script = "selectfilter.%s('%s', '%s', '%s', '%s', '%s')" % (
				js_method_name,
				element_id,
				model._meta.app_label,
				model._meta.object_name,
				utils.lookupToString(lookup_dict),
				select_related)
			if index == default_index:
				return '<option selected="selected" value="%s">%s</option> '% (script, label)
			return '<option value="%s">%s</option> '% (script, label)
		return '<select onChange="eval(this.value)">%s</select>' % "\n".join(renderElement(index, lookup) for index, lookup in enumerate(lookups))

	def composeField(self, lookups_output, parent_output):
		"""Composes HTML code for entire field from both filter and selection widget's HTML elements."""
		return u"""
			<div class="field-box">
			%s
			<p></p>
			%s
			</div>""" % (lookups_output, parent_output)

class HyperLinksFilter(object):

	def renderFilter(self, js_method_name, element_id, model, lookups, select_related, *args, **kwargs):
		if len(lookups) <= 1:
			return ""
		def renderElement(lookup):
			label, lookup_dict = lookup
			script = "selectfilter.%s('%s', '%s', '%s', '%s', '%s')" % (
				js_method_name,
				element_id,
				model._meta.app_label,
				model._meta.object_name,
				utils.lookupToString(lookup_dict),
				select_related)
			return '<a class="ajax_filter_choice" href="javascript:void(0)"onclick="%s">%s</a>'% (script, label)
		return "\n".join(renderElement(lookup) for lookup in lookups)

	def composeField(self, lookups_output, parent_output):
		"""Composes HTML code for entire field from both filter and selection widget's HTML elements."""
		return u"""
			<div>
				%s
			</div>
			%s
			""" % (lookups_output, parent_output)


class FilteredSelectMultiple(forms.SelectMultiple):

	def render(self, name, value, attrs=None, choices=()):
		self._element_id = attrs['id']
		# choices links
		# if there is only one choice, then nothing will be rendered
		lookups = utils.getLookups(self.lookups)
		lookups_output = self.filter_widget.renderFilter("getManyToManyJSON", self._element_id, self.model, lookups, self.select_related, self.default_index)
		
		# normal widget output from the anchestor
		self.choices = self._getAllChoices(value)
		parent_output = super(FilteredSelectMultiple, self).render(name, value, attrs, choices)
		
		# create the output including the django admin's Javascript code that
		# mutates the select widget into a selectfilter one
		# this assumes that /admin/jsi18n/, core.js, SelectBox.js and
		# SelectFilter2.js are loaded from the page
		verbose_name = self.model._meta.verbose_name_plural.replace('"', '\\"')
		
		output = u"""
			%s
			<script type="text/javascript">
				(function($) {
					$(document).ready(function(){
						SelectFilter.init("id_%s", "%s", 0, "%s");
					});
				})(django.jQuery);
			</script>
		""" % (self.filter_widget.composeField(lookups_output, parent_output), name, 
			verbose_name, settings.ADMIN_MEDIA_PREFIX)
		
		return mark_safe(output)
		
	def _getAllChoices(self, value):
		value = value or []
		choices = list(self.choices)
		# convert to unicode for safe comparisong during a ValidationError
		choices_keys = [unicode(i[0]) for i in choices]
		objects_to_fetch = []
		for i in value:
			if not unicode(i) in choices_keys:
				objects_to_fetch.append(i)
		if objects_to_fetch:
			objects = utils.getObjects(self.model, {"pk__in": objects_to_fetch}, self.select_related)
			for obj in objects:
				choices.append((obj.pk, unicode(obj)))
		choices.sort(key=operator.itemgetter(1))
		return choices

