let apm
let rpm
let reload



window.setInterval(
    ()=>{
        $.ajax({
            url:'test',
            headers: {
                'Apm':apm,
                'Rpm': rpm,
            },
            type: 'GET',
            success: function(response){
                console.log(response.data)
                if(response.data.val){
                    location.reload()
                }
                else{
                    apm = response.data.tapm
                    rpm = response.data.trpm
                }
            },
            error: function(response){
                console.log('error: ', response.error)
            }
        })
    }
,
60000
)

$.ajax({
    type: 'GET',
    url:'home_chart',
    success: function(response){
        apm = response.data.tapm
        rpm = response.data.trpm
        chart = response.data.chart
        if(chart === undefined)
        {
        }
        else{
            const chartcontainer = document.getElementById("graph-container")        
            chartcontainer.innerHTML+=`<img src="${chart}" class="chart" />`
        }
    },
    error: function(response){
        console.log('error: ', response.error)
    }
})

