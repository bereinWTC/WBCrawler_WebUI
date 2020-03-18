$(document).ready(function () {
    
    $('#container').highcharts({
        chart: charts,
        title: title,
        xAxis: xAxis,
        yAxis: yAxis,
        series: series,
        tooltip:{
             formatter: function() {

                 return '<b>'+this.point.series.name+'</b><br /><b>'+ Highcharts.numberFormat(this.point.x, 0)+','+Highcharts.numberFormat(350-this.point.y, 0) +'</b>';
             }
         }

    });

     
//     $('#container').highcharts({
//         chart: json.chart,
//         title: json.title,
//         xAxis: json.xAxis,
//         yAxis: json.yAxis,
//         series: json.series,
//         // tooltip:{
//      //        headerFormat: '<b>{series.name}</b>{point.series}<br>',
//      //        pointFormat: '{point.x}, {point.y}'
//      //    }
//         tooltip:{
//             formatter: function() {

//                 return '<b>'+this.point.series.name+'</b><br/><b>'+this.point.name+'</b><br /><b>'+ Highcharts.numberFormat(this.point.x, 0)+','+Highcharts.numberFormat(350-this.point.y, 0) +'</b>';
//             }
//         }
//     });

   

});

// var chart = new Highcharts.Chart({
//     chart: chart,
//     title: title,
//     xAxis: xAxis,
//     yAxis: yAxis,
//     series: series,
//     tooltip:{
//          formatter: function() {

//              return '<b>'+this.point.series.name+'</b><br/><b>'+this.point.name+'</b><br /><b>'+ Highcharts.numberFormat(this.point.x, 0)+','+Highcharts.numberFormat(this.point.y, 0) +'</b>';
//          }
//      }

// })
// $(document).ready(function() {
// 	$('#container').highcharts({
// 		chart: chart,
// 		title: title,
// 		xAxis: xAxis,
// 		yAxis: yAxis,
// 		series: series,
// 		// tooltip:{
// 	 //        headerFormat: '<b>{series.name}</b>{point.series}<br>',
// 	 //        pointFormat: '{point.x}, {point.y}'
// 	 //    }
// 	 	tooltip:{
// 	 		formatter: function() {

// 				return '<b>'+this.point.series.name+'</b><br/><b>'+this.point.name+'</b><br /><b>'+ Highcharts.numberFormat(this.point.x, 0)+','+Highcharts.numberFormat(this.point.y, 0) +'</b>';
// 			}
// 	 	}
// 	});
// });
