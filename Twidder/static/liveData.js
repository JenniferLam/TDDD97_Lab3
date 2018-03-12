setupGraph = function() {
	var numPost_config = liquidFillGaugeDefaultSettings();
    numPost_config.displayPercent = false;
    graph_numPost = loadLiquidFillGauge("graph_numPost", 0, numPost_config);
}

updateGraph = function(graphObject, number) {
	graphObject.update(number);
}
