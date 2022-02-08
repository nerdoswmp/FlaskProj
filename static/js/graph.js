function cb(selection) {
    req = $.ajax({
        url: "/callback",
        type: "POST",
        data: { 'data': selection },
    });

    req.done(function(result) {
        var graphs = JSON.parse(result);
        Plotly.react('chart', graphs, {});
    });
}