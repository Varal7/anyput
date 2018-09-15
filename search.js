'use strict';

var host = window.location.host;
var ws = new WebSocket('ws://'+host+'/ws');

var $message = $('#message');
var $output = $('#output')[0];
var $connexions = $('#connexions');


ws.onopen = function(){
    $message.attr("class", 'label label-success');
    $message.text('open');
};

ws.onmessage = function(ev){
    var json = JSON.parse(ev.data);
    if (json.type == 'output') {
        appendOutput(json.value);
    }
    else if (json.type == 'clear') {
        clearOutput();
    }
    else if (json.type == 'nb_clients') {
        updateClient(json.value);
    }
};

ws.onclose = function(ev){
    $message.attr("class", 'label label-important');
    $message.text('closed');
};
ws.onerror = function(ev){
    $message.attr("class", 'label label-warning');
    $message.text('error occurred');
};


function appendOutput(value) {
    var cur = $output.innerHTML;
    $output.innerHTML = (cur + value + '\n');
}

function updateClient(nb_clients) {
    $connexions.text(nb_clients);
}
