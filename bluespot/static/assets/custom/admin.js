function PlotPieGraphAdmin(){
	var data = [];
	var series = Math.floor(Math.random() * 10) + 1;
	series = series < 5 ? 5 : series;
	for (var i = 0; i < series; i++) {
		data[i] = {
			label: "Series" + (i + 1),
			data: Math.floor(Math.random() * 100) + 1
		};
	}
	$.plot($("#pie_devices"), data, {
                    series: {
                        pie: {
                            show: true
                        }
                    },
                    legend: {
                        show: false
                    }                    
	});
    $.plot($("#pie_ages"), data, {
                    series: {
                        pie: {
                            show: true
                        }
                    },
                    legend: {
                        show: false
                    }
    });
    $.plot($("#pie_social"), data, {
                    series: {
                        pie: {
                            show: true
                        }
                    },
                    legend: {
                        show: false
                    }
    });
}


