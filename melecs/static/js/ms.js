const table = document.getElementById("table")
const origin = window.location.origin


start("Date")
function start(order){
    table.innerHTML = `
    <tr>
        <th>Mérési azonosító</th>
        <th>Mérés Dátuma</th>
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
                    <tr class="item" item-id="${item.ID}">
                        <th class="">${item.ID}</th>
                        <th class="">${item.date}</th>
                        <th class="">${item.active}</th>
                    </tr>
                    <div class="non-visible detail" id="${item.ID}"></div>
                `
            });
            get_details()
        },
        error: function(response){
            console.log('error: ', response.error)
        }
    });
}

function get_details (){
        items = [...document.getElementsByClassName("item")]
        details = [...document.getElementsByClassName("detail")]
        console.log(origin)
        $(items).click(function(){
            msid = $(this).attr("item-id")
            console.log($(this).attr("item-id"))
            $.ajax({
                type: 'GET',
                url:`${origin}/msdetails/${msid}/`,
                success: function(response){
                   console.log(response)
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
                                percent=String(((dpm/rpm).toFixed(4))*100)+"  %"
                            }
                            else{
                                percent="ismeretlen"
                            }
    
                            e.innerHTML=`
                            <div class="detail-list">
                                <div class="d-group">
                                    <div class="d-group-title">Általános információk</div>
                                    <div class="d-group-elements">
                                        <div class="d-list-item">Mérést végző személy:<div class="d-list-data">${person}</div></div>
                                        <div class="d-list-item">Mérés helyszíne:<div class="d-list-data">${place}</div></div>
                                    </div>
                                </div>
                                <div class="d-group">
                                    <div class="d-group-title">Mérési Adatok</div>
                                        <div class="d-list-item">Mérések száma: <div class="d-list-data">${msammount}</div></div>
                                        <div class="d-list-item">Mérések értéke:<div class="d-list-data">${sum}</div></div>
                                        <div class="d-list-item">Százalékos teljesítés*: <div class="d-list-data">${percent}</div></div>
                                    <div class="d-group-elements"></div>
                                </div>
                                <div class="d-group">
                                    <div class="d-group-title">Idő adatok</div>
                                    <div class="d-group-elements">
                                        <div class="d-list-item">Kezdés:<div class="d-list-data">${starttime}</div></div>
                                        <div class="d-list-item">Befejezés:<div class="d-list-data">${endtime}</div></div>
                                    </div>
                                </div>
                            </div>
                            <div class="d-footnote">* Teljesített/Elvárt százalékos aránya.</div>
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