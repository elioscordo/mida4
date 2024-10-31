import { Vue } from 'vue';

import SymbolChart from './components/SymbolChart.vue'

console.log('main')

$('.symbol-chart').each(function () {
    var $el = $(this)
    var data = $el.data()
    var id = $el.attr('id')
    new Vue({
        'el': `#${id}`,
        'render': (h) => {
            return h(SymbolChart,{data})
        }
    });
});
