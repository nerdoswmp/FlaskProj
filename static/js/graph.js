/*

d = {{ graphJSON | safe }};

function cb(selection) {
    $.getJSON({
        url: "/callback", data: { 'data': selection }, success: function (result) {
            Plotly.newPlot('chart', result, {staticPlot: true});;
        }
    });
}

setInterval(cb(d), 5000);


não to conseguindo fazer o gráfico atualizar via função ent é nois
*/