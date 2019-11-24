var url = "/names";
var urlS = "/samples/943";
var urlM = '/metadata/943';

var selector = d3.select("#selDataset");
var sele = d3.select("#sample-metadata");
sele.html("");
// ----------------------------------
d3.json(url).then(function(sampleN) {
    sampleN.forEach(function(sam){
        selector
            .append("option")
            .text(sam)
            .property("value", sam);   
    })
    var firstS = sampleN[0]
    optionChanged(firstS)
    sele.html("");
    // charts(firstS)
});
// ----------------------------------
function optionChanged(newSample){
    charts(newSample)
    return(newSample);
};
// -----------------------------------
function charts(sample){
    d3.json(`/samples/${sample}`).then(function(data){
        var tracePie = {
            labels: data.otu_id,
            values: data.Percentage,
            mode: "markers",
            marker: {size: 12},
            // hovertemplate: '<b>%{text}</b>',
            // text: data.out_label,
            type : "pie"
        };
        var layoutPie = {
            autosize: false,
            width: 500,
            height: 500,
            title: "Sample Values"
            };
        Plotly.newPlot("pie", [tracePie], layoutPie);

    });
    d3.json(`/metadata/${sample}`).then(function(datax){
        sele.html("");
        Object.entries(datax).forEach(([key, value]) => {
            sele.append("p").text(`${key}: ${value}`);
        });
    });
};
// -----------------------------------






