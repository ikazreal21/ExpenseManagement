"use strict";
document.addEventListener("DOMContentLoaded", function () {



    // Spinner
    var spinner = function () {
      setTimeout(function () {
            document.getElementById('spinner').style.display = "none";
            document.getElementById('data').style.display = "block";
      }, 3000);
      document.getElementById('spinner').style.display = "none";
      document.getElementById('data').style.display = "block";
    };


    var myVar;
    function myFunction() {
        // myVar = setTimeout(showPage, 2000);
        console.log("hello")
    }
      
    // function showPage() {
    //     document.getElementById("data").style.display = "none";
    //     document.getElementById("spinner").style.display = "block";
      
    //   }
    // spinner();
 


    // var PIECHARTEXMPLE = document.getElementById("pieChartExample1");
    // var pieChartExample1 = new Chart(PIECHARTEXMPLE, {
    //     type: "pie",
    //     data: {
    //         labels: ["A", "B", "C", "D"],
    //         datasets: [
    //             {
    //                 data: [300, 50, 100, 80],
    //                 borderWidth: 0,
    //                 backgroundColor: ["#44b2d7", "#59c2e6", "#71d1f2", "#96e5ff"],
    //                 hoverBackgroundColor: ["#44b2d7", "#59c2e6", "#71d1f2", "#96e5ff"],
    //             },
    //         ],
    //     },
    // });

    // var pieChartExample1 = {
    //     responsive: true,
    // };


    // ------------------------------------------------------- //
    // Line Chart
    // ------------------------------------------------------ //
    var legendState = true;
    if (window.outerWidth < 576) {
        legendState = false;
    }
    
    var canvas = document.querySelector("canvas");

    var ctx1 = canvas.getContext("2d");
    var gradient1 = ctx1.createLinearGradient(150, 0, 150, 300);
    gradient1.addColorStop(0, "rgba(133, 180, 242, 0.91)");
    gradient1.addColorStop(1, "rgba(255, 119, 119, 0.94)");

    const expenses = JSON.parse(document.getElementById('total_expenses_per_month').textContent);
    var LINECHART = document.getElementById('lineCahrt');
    var myLineChart = new Chart(LINECHART, {
        type: "line",
        options: {
            legend: { display: false },
            scales: {
                xAxes: [
                    {
                        display: true,
                        gridLines: {
                            color: "#eee",
                        },
                    },
                ],
                yAxes: [
                    {
                        display: true,
                        gridLines: {
                            color: "#eee",
                        },
                    },
                ],
            },
        },
        data: {
            labels: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
            datasets: [
                {
                    label: "Expenses Per Year",
                    fill: true,
                    lineTension: 0.5,
                    backgroundColor: gradient1,
                    borderColor: gradient1,
                    pointBorderColor: '#da4c59',
                    pointHoverBackgroundColor: '#da4c59',
                    borderCapStyle: 'butt',
                    borderDash: [],
                    borderDashOffset: 0.0,
                    borderJoinStyle: 'miter',
                    borderWidth: 1,
                    pointHoverBackgroundColor: gradient1,
                    pointHoverBorderColor: "rgba(220,220,220,1)",
                    pointBorderWidth: 1,
                    pointHoverRadius: 5,
                    pointHoverBorderColor: "#fff",
                    pointHoverBorderWidth: 2,
                    pointRadius: 1,
                    pointHitRadius: 10,
                    data: expenses,
                    spanGaps: false
                },
            ],
        }
    });



    const category = JSON.parse(document.getElementById('chart_category').textContent);
    const category_expeses = JSON.parse(document.getElementById('chart_category_epenses').textContent);

    
    var PIECHARTEXMPLE = document.getElementById("pieChartExample");
    var pieChartExample = new Chart(PIECHARTEXMPLE, {
        type: "pie",
        data: {
            labels: category,
            datasets: [
                {
                    data: category_expeses,
                    borderWidth: 0,
                    backgroundColor: ["blue", "red", "green", "violet"],
                    hoverBackgroundColor: ["lightblue", "lightred", "lightgreen", "lightviolet"],
                },
            ],
        },
    });

    var pieChartExample = {
        responsive: true,
    };


    // ------------------------------------------------------- //
    // Line Chart 1
    // ------------------------------------------------------ //
    var LINECHART1 = document.getElementById('lineChart1');
    var myLineChart = new Chart(LINECHART1, {
        type: 'line',
        options: {
            scales: {
                xAxes: [{
                    display: true,
                    gridLines: {
                        display: false
                    }
                }],
                yAxes: [{
                    ticks: {
                        max: 40,
                        min: 0,
                        stepSize: 0.5
                    },
                    display: false,
                    gridLines: {
                        display: false
                    }
                }]
            },
            legend: {
                display: false
            }
        },
        data: {
            labels: ["A", "B", "C", "D", "E", "F", "G"],
            datasets: [
                {
                    label: "Total Overdue",
                    fill: true,
                    lineTension: 0,
                    backgroundColor: "transparent",
                    borderColor: '#6ccef0',
                    pointBorderColor: '#59c2e6',
                    pointHoverBackgroundColor: '#59c2e6',
                    borderCapStyle: 'butt',
                    borderDash: [],
                    borderDashOffset: 0.0,
                    borderJoinStyle: 'miter',
                    borderWidth: 3,
                    pointBackgroundColor: "#59c2e6",
                    pointBorderWidth: 0,
                    pointHoverRadius: 4,
                    pointHoverBorderColor: "#fff",
                    pointHoverBorderWidth: 0,
                    pointRadius: 4,
                    pointHitRadius: 0,
                    data: [20, 28, 30, 22, 24, 10, 7],
                    spanGaps: false
                }
            ]
        }
    });



    // ------------------------------------------------------- //
    // Pie Chart
    // ------------------------------------------------------ //
    var PIECHART = document.getElementById('pieChart');
    var myPieChart = new Chart(PIECHART, {
        type: 'doughnut',
        options: {
            cutoutPercentage: 80,
            legend: {
                display: false
            }
        },
        data: {
            labels: [
                "First",
                "Second",
                "Third",
                "Fourth"
            ],
            datasets: [
                {
                    data: [300, 50, 100, 60],
                    borderWidth: [0, 0, 0, 0],
                    backgroundColor: [
                        '#44b2d7',
                        "#59c2e6",
                        "#71d1f2",
                        "#96e5ff"
                    ],
                    hoverBackgroundColor: [
                        '#44b2d7',
                        "#59c2e6",
                        "#71d1f2",
                        "#96e5ff"
                    ]
                }]
        }
    });


    // ------------------------------------------------------- //
    // Bar Chart
    // ------------------------------------------------------ //
    var BARCHARTHOME = document.getElementById('barChartHome');
    var barChartHome = new Chart(BARCHARTHOME, {
        type: 'bar',
        options:
        {
            scales:
            {
                xAxes: [{
                    display: false
                }],
                yAxes: [{
                    display: false
                }],
            },
            legend: {
                display: false
            }
        },
        data: {
            labels: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "November", "December"],
            datasets: [
                {
                    label: "Data Set 1",
                    backgroundColor: [
                        'rgb(121, 106, 238)',
                        'rgb(121, 106, 238)',
                        'rgb(121, 106, 238)',
                        'rgb(121, 106, 238)',
                        'rgb(121, 106, 238)',
                        'rgb(121, 106, 238)',
                        'rgb(121, 106, 238)',
                        'rgb(121, 106, 238)',
                        'rgb(121, 106, 238)',
                        'rgb(121, 106, 238)',
                        'rgb(121, 106, 238)',
                        'rgb(121, 106, 238)'
                    ],
                    borderColor: [
                        'rgb(121, 106, 238)',
                        'rgb(121, 106, 238)',
                        'rgb(121, 106, 238)',
                        'rgb(121, 106, 238)',
                        'rgb(121, 106, 238)',
                        'rgb(121, 106, 238)',
                        'rgb(121, 106, 238)',
                        'rgb(121, 106, 238)',
                        'rgb(121, 106, 238)',
                        'rgb(121, 106, 238)',
                        'rgb(121, 106, 238)',
                        'rgb(121, 106, 238)'
                    ],
                    borderWidth: 1,
                    data: [35, 49, 55, 68, 81, 95, 85, 40, 30, 27, 22, 15]
                }
            ]
        }
    });

});
