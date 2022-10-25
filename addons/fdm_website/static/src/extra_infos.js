odoo.define('fdm_website.datepickerExtra', function (require) {
'use strict';
var publicWidget = require('web.public.widget');
var time = require('web.time');

publicWidget.registry.datepicker = publicWidget.Widget.extend({
    selector: '.datetimepickerExtraInfo',

    start: function () {
        this._initDateTimePicker($('#datetimepickerExtraInfo'));
        return this._super.apply(this, arguments)
    },

    _initDateTimePicker: function ($dateGroup) {
        var minDateData = $dateGroup.data('mindate');
        var datetimepickerFormat = time.getLangDateFormat();
        var minDate = minDateData;
        $dateGroup.datetimepicker({
            format : datetimepickerFormat,
            minDate: minDate,
        });


    },

});

});

