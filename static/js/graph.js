/* globals Chart:false, feather:false */

(() => {
    'use strict'
  
    
    window.chartColors = {
        red: 'rgb(255, 99, 132)',
        orange: 'rgb(255, 159, 64)',
        yellow: 'rgb(255, 205, 86)',
        green: 'rgb(75, 192, 192)',
        blue: 'rgb(54, 162, 235)',
        purple: 'rgb(153, 102, 255)',
        grey: 'rgb(201, 203, 207)'
    };
  
    const ctx = document.getElementById('myChart')
  
    const myChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: [
                'negative',
                'positive',
                'neutral'],
            datasets: [{
            data: [
                23,
                17,
                4
            ],
            lineTension: 0,
            backgroundColor: [
                window.chartColors.red,
                window.chartColors.blue,
                window.chartColors.grey,
            ],
            borderColor: '#007bff',
            borderWidth: 0,
            }]
        },
        options: {
            responsive: true,
            legend: {
                position: 'bottom',
            }
        }
    })
})
  