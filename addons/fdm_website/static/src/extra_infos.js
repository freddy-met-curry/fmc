odoo.define('fdm_website.datepickerExtraInfo', function (require) {
'use strict';
var publicWidget = require('web.public.widget');
var time = require('web.time');
var core = require('web.core');
var Dialog = require('web.Dialog');
var dom = require('web.dom');
var field_utils = require('web.field_utils');

var _t = core._t;

publicWidget.registry.datepickerExtraInfo = publicWidget.Widget.extend({
    selector: '.datetimepickerExtraInfo',

    /**
     * @override
     */
    start: function () {
        console.log('test 1');
        this._initDateTimePicker($('#datetimepickerExtraInfo'));
    },
    _formatDateTime: function (datetimeValue, format){
        return moment(field_utils.format.datetime(moment(datetimeValue), null, {timezone: true}), format);
    },

    _initDateTimePicker: function ($dateGroup) {
        console.log('test');
        var disabledDates = [];
        var questionType = $dateGroup.find('input').data('questionType');
        var minDateData = $dateGroup.data('mindate');
        var maxDateData = $dateGroup.data('maxdate');

        var datetimepickerFormat = questionType === 'datetime' ? time.getLangDatetimeFormat() : time.getLangDateFormat();

        var minDate = minDateData
            ? this._formatDateTime(minDateData, datetimepickerFormat)
            : moment({ y: 1000 });

        var maxDate = maxDateData
            ? this._formatDateTime(maxDateData, datetimepickerFormat)
            : moment().add(200, "y");

        if (questionType === 'date') {
            // Include min and max date in selectable values
            maxDate = moment(maxDate).add(1, "d");
            minDate = moment(minDate).subtract(1, "d");
            disabledDates = [minDate, maxDate];
        }

        $dateGroup.datetimepicker({
            format : datetimepickerFormat,
            minDate: minDate,
            maxDate: maxDate,
            disabledDates: disabledDates,
            useCurrent: false,
            viewDate: moment(new Date()).hours(minDate.hours()).minutes(minDate.minutes()).seconds(minDate.seconds()).milliseconds(minDate.milliseconds()),
            calendarWeeks: true,
            icons: {
                time: 'fa fa-clock-o',
                date: 'fa fa-calendar',
                next: 'fa fa-chevron-right',
                previous: 'fa fa-chevron-left',
                up: 'fa fa-chevron-up',
                down: 'fa fa-chevron-down',
            },
            locale : moment.locale(),
            allowInputToggle: true,
        });
        $dateGroup.on('error.datetimepicker', function (err) {
            if (err.date) {
                if (err.date < minDate) {
                    Dialog.alert(this, _t('The date you selected is lower than the minimum date: ') + minDate.format(datetimepickerFormat));
                }

                if (err.date > maxDate) {
                    Dialog.alert(this, _t('The date you selected is greater than the maximum date: ') + maxDate.format(datetimepickerFormat));
                }
            }
            return false;
        });
    },

});

});
