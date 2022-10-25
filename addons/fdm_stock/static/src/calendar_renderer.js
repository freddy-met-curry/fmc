odoo.define('fred_stock.CalendarRenderer', function (require) {
"use strict";

const {qweb} = require('web.core');

const CalendarRenderer = require('web.CalendarRenderer');
CalendarRenderer.include({
        _getFullCalendarOptions: function () {
            const options = this._super(...arguments);
            var self = this;
            return Object.assign(options, {
            eventRender: function (info) {
                var event = info.event;
                var element = $(info.el);
                var view = info.view;
                if (self && self.model && self.model === 'stock.picking'){
                    if (event && event.extendedProps && event.extendedProps.record && event.extendedProps.record.partner_id){
                            event.extendedProps.record.display_name = event.extendedProps.record.partner_id[1]
                    }
                }
                self._addEventAttributes(element, event);
                if (view.type === 'dayGridYear') {
                    const color = this.getColor(event.extendedProps.color_index);
                    if (typeof color === 'string') {
                        element.css({
                            backgroundColor: color,
                        });
                    } else if (typeof color === 'number') {
                        element.addClass(`o_calendar_color_${color}`);
                    } else {
                        element.addClass('o_calendar_color_1');
                    }
                } else {
                var $render = $(self._eventRender(event));
                element.find('.fc-content').html($render.html());
                element.addClass($render.attr('class'));

                // Add background if doesn't exist
                if (!element.find('.fc-bg').length) {
                    element.find('.fc-content').after($('<div/>', {class: 'fc-bg'}));
                }

                if (view.type === 'dayGridMonth' && event.extendedProps.record) {
                    var start = event.extendedProps.r_start || event.start;
                    var end = event.extendedProps.r_end || event.end;
                    $(this.el).find(_.str.sprintf('.fc-day[data-date="%s"]', moment(start).format('YYYY-MM-DD'))).addClass('fc-has-event');
                    // Detect if the event occurs in just one day
                    // note: add & remove 1 min to avoid issues with 00:00
                    var isSameDayEvent = moment(start).clone().add(1, 'minute').isSame(moment(end).clone().subtract(1, 'minute'), 'day');
                    if (!event.extendedProps.record.allday && isSameDayEvent) {
                        // For month view: do not show background for non allday, single day events
                        element.addClass('o_cw_nobg');
                        if (event.extendedProps.showTime && !self.hideTime) {
                            const displayTime = moment(start).clone().format(self._getDbTimeFormat());
                            element.find('.fc-content .fc-time').text(displayTime);
                        }
                    }
                }

                // On double click, edit the event
                element.on('dblclick', function () {
                    self.trigger_up('edit_event', {id: event.id});
                });
                }
            },

                });
        },

});

});
