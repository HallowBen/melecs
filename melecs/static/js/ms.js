const table = document.getElementById("table")
const origin = window.location.origin
const search = document.getElementById("search")
data=[]
where=document.getElementById("where")
current_order="Date"
prev_order = "Date"

start(current_order)
function start(order){
ordered = document.getElementById("ordered")
ordered.innerHTML=`Rendezve: ${current_order}`
    table.innerHTML = `
    <tr>
        <th id="ID" class="order">Mérési azonosító</th>
        <th id="Date" class="order">Mérés Dátuma</th>
        <th>Státusz</th>
    </tr>
    `
    get_data(order)
}


function get_data(order){
    $.ajax({
        type: "GET",
        url: `${origin}/msdata/${order}`,
        success: function (response) {
            data = response.data
            data.forEach(item => {
                table.innerHTML+=`
                <hr class="t-line">
                    <tr class="item" item-id="${item.ID}">
                        <td class="">${item.ID}</td>
                        <td class="">${item.date}</td>
                        <td class="">${item.active}</td>
                    </tr>
                    <div class="non-visible detail" id="${item.ID}"></div>
                `
            });
            get_details()
            restart()
        },
        error: function(response){
            console.log('error: ', response.error)
        }
    });
}

function get_details (){
        items = [...document.getElementsByClassName("item")]
        details = [...document.getElementsByClassName("detail")]
        $(items).click(function(){
            msid = $(this).attr("item-id")
            $.ajax({
                type: 'GET',
                url:`${origin}/msdetails/${msid}/`,
                success: function(response){
                   data = response.data
                   details.forEach(e => {
                    if(e.id === msid){
                        if(e.classList.contains("open")){
                            e.innerHTML=""
                            e.classList.remove("open")
                            e.classList.add("non-visible")
                        }
                        else{
                            e.classList.add("open")
                            e.classList.remove("non-visible")
                            required=data.required
                            person=data.person
                            place=data.place
                            sum=data.SUM
                            measuredtime=data.measuredtime
                            endtime=data.Endtime
                            starttime=data.Start_Time
                            msammount = data.msammount
                            if (typeof required ==='number'){
                                dpm=sum/(measuredtime/60)
                                rpm=required/60
                                percent=String(((dpm/rpm).toFixed(2))*100)+"  %"
                            }
                            else{
                                percent="ismeretlen"
                            }
    
                            e.innerHTML=`
                            <table>
                                <tr>
                                <th>Általános információk</th>
                                <th>Mérési Adatok</th>
                                <th>Idő adatok</th>
                                </tr>
                                <tr>
                                <td>Mérést végző személy: ${person}</td>
                                <td>Mérések értéke: ${sum}</td>
                                <td>Kezdés: ${starttime}</td>
                                </tr>
                                <tr>
                                <td>Mérés helyszíne: ${place}</td>
                                <td>Százalékos teljesítés*: ${percent}</td>
                                <td>Befejezés: ${endtime}</td>
                                </tr>
                                <tr>
                                <td>Mérések száma: ${msammount}</td>
                                <td></td>
                                <td></td>
                                </tr>
                            </table>
                                <div>* Teljesített/Elvárt százalékos aránya.</div>
                            `
                        }
                        
                    }
                });
                },
                error: function(response){
                    console.log('error: ', response.error)
                }
            })
        })
    }

    function restart(){
        
        order = [...document.getElementsByClassName("order")]
        $(order).click(function () { 
            if(this.id === current_order){
                prev_order=current_order
                current_order=`-${current_order}`
                start(current_order)
            }
            else if(this.id === prev_order){
                current_order=prev_order
                prev_order=`-${current_order}`
                start(current_order)
            }
            else{
                prev_order=current_order
                current_order=this.id
                start(current_order)
            }
            });
    }
;(function(){
    search_box = document.getElementById("search_box")
        search_box.innerHTML=`<input id="what" type="text" placeholder="Keresés.. " required>`
})()
$(where).change(function (e) { 
    e.preventDefault();
    console.log(where.value)
    if(where.value === 'Date'){
        search_box = document.getElementById("search_box")
        today = new Date()
        search_box.innerHTML=`
            <input id="what" type="text"
            pattern="\^(([0-9]{2}))$\" placeholder="dd" required > 
        `
    }
    else{
        search_box = document.getElementById("search_box")
        search_box.innerHTML=`<input id="what" type="text" placeholder="Keresés.. " required>`
    }
});

$(search).submit(function (e) { 
    e.preventDefault();
    wherev = where.value
    what=document.getElementById("what").value
    if(wherev==="Date"){
        date = new Date()
        date.setDate(what)
        what = date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + (date.getDate() >= 10 ? date.getDate() : "0" + date.getDate())
    }
    searched(wherev,what)
});



function searched(wh,wa){
    $.ajax({
        type: "GET",
        url:`${origin}/mssearch/${wh}/${wa}`,
        success: function (response) {
            data = response.data
            console.log(data)
        },
        error: function(response){
            console.log('error: ', error)
        }
    });
}


//\^(([0-9]{4}|*)\-([0-9]{2}|*)\-([0-9]{2}|*))$\
//const year_pattern = /^(([0-9]{4}|\*))$/g
//const month_pattern = /^(([0-9]{4}|\*)\-([0-9]{2}|\*))$/g