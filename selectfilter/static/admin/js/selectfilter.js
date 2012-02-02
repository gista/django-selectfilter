(function($) {
	selectfilter = {
		request_url: "/selectfilter/json_index/",
		data_loaded: "data_loaded",

		_appendOption: function(obj, selector) {
			// append a json data row as an option to the selector
			var option = $('<option>' + obj[1] + '</option>');
			option.attr({value: obj[0]});
			option.appendTo(selector);
			return option;
		},

		_removeOptions: function(selector) {
			// remove all options from selector
			selector.children("option").each(function(i) {
				$(this).remove();
			});
		},

		getManyToManyJSON: function(element_id, app_label, object_name, 
			lookup_string, select_related) {
			// manage the ManyToMany ajax request
			var selector_from = $("#" + element_id + "_from");
			var selector_to = $("#" + element_id + "_to");
		
			$("#" + element_id + "_input").val("");
			selector_from.attr("disabled", true);
			selector_to.attr("disabled", true);

			this._removeOptions(selector_from);
		
			$.getJSON(this.request_url, {
				app_label: app_label, 
				object_name: object_name, 
				lookup_string: lookup_string,
				select_related: select_related},
				function(data){
					selectfilter._removeOptions(selector_from);
					$.each(data, function(i, obj){
						var option_is_selected = selector_to.children("option[value='" + obj[0] + "']").length;
						if (!option_is_selected) {
							selectfilter._appendOption(obj, selector_from);
						};
					});
					SelectBox.init(element_id + "_from");
					selector_from.attr("disabled", false);
					selector_to.attr("disabled", false);
					selector_from.trigger(selectfilter.data_loaded);
				});
		}
	};
})(django.jQuery);
