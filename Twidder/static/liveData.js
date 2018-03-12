

setupGraph = function(max_users) {
	var config_numPost = liquidFillGaugeDefaultSettings();
    config_numPost.displayPercent = false;
	config_numPost.waveAnimateTime = 5000;
	config_numPost.waveHeight = 0.08;
	config_numPost.waveCount = 2;
	config_numPost.textVertPosition = 0.75;
	config_numPost.waveAnimate = true;
	config_numPost.maxValue = 100;
    graph_numPost = loadLiquidFillGauge("graph_numPost", 0, config_numPost);
	var config_numUsers = liquidFillGaugeDefaultSettings();
    config_numUsers.displayPercent = false;
	config_numUsers.circleColor = "#246D5F";
    config_numUsers.textColor = "#0E5144";
    config_numUsers.waveTextColor = "#91bab2";
    config_numUsers.waveColor = "#246D5F";
	config_numUsers.waveAnimateTime = 5000;
	config_numUsers.waveHeight = 0.08;
	config_numUsers.waveCount = 2;
	config_numUsers.textVertPosition = 0.75;
	config_numUsers.waveAnimate = true;
	config_numUsers.maxValue = 100;
	graph_numUsers = loadLiquidFillGauge("graph_numUsers", 0, config_numUsers);
	var config_attraction = liquidFillGaugeDefaultSettings();
    config_attraction.displayPercent = false;
	config_attraction.circleColor = "#FF4D4D";
    config_attraction.textColor = "#FF3333";
    config_attraction.waveTextColor = "#FFE6E6";
    config_attraction.waveColor = "#FF4D4D";
	config_attraction.waveAnimateTime = 5000;
	config_attraction.waveHeight = 0.08;
	config_attraction.waveCount = 2;
	config_attraction.textVertPosition = 0.75;
	config_attraction.waveAnimate = true;
	config_attraction.maxValue = 100;
	graph_attraction = loadLiquidFillGauge("graph_attraction", 0, config_attraction);
}

updateGraph = function(graphObject, number, max_value) {
	graphObject.update(number,max_value);
}
