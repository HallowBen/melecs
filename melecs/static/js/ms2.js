const table = document.getElementById("table")
const origin = window.location.origin
const search_box = document.getElementById("search")
var full_data=[]
var data = []
current_order="ID"
prev_order = ""


;(function(){
    $.ajax({
        type: "GET",
        url: `${origin}/msdata/`,
        success: function (response) {
            full_data=response.data
            data = JSON.parse(JSON.stringify(full_data))
            ordered()
        },
        errro: function (response){
            console.error(response);
        },
    });
})()

function ordered(){
    if(current_order != prev_order){
        prev_order = current_order
        data.sort(function(a,b){
        return a[current_order] > b[current_order];
        })
        ordered_space = document.getElementById("ordered")
        ordered_space.innerHTML =`Rendezve: ${current_order}`
    }
    else{
        prev_order = "-" + current_order
        data.sort(function(a,b){
        return a[current_order] < b[current_order];
        })
        ordered_space = document.getElementById("ordered")
        ordered_space.innerHTML =`Rendezve: ${prev_order}`
    } 
    scr_out()

}

function scr_out(){
        table.innerHTML = `
        <tr>
            <th id="ID" class="order">Mérési azonosító</th>
            <th id="Date" class="order">Mérés Dátuma</th>
            <th>Státusz</th>
        </tr>
        `
        data.forEach(item => {
                table.innerHTML+=`
                <hr class="t-line">
                    <tr class="item" item-id="${item.ID}">
                        <td class="">${item.ID}</td>
                        <td class="">${item.Date}</td>
                        <td class="">${item.active}</td>
                    </tr>
                    <div class="non-visible detail" id="${item.ID}"></div>
                `
        });
        get_details()
        restart()
}

function restart(){
    $(".order").click(function(){
        current_order=this.id
        ordered()
    })
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

function search(sstr){
    sstr = sstr.toString().toLowerCase()
    if(sstr=="\"\""){
        data = JSON.parse(JSON.stringify(full_data))
    }
    else{
        indexes = []
        full_data.forEach((e,i) => {
            dstr = e.ID.toString().toLowerCase()
            if(dstr.includes(sstr) && !(indexes.includes(i))){
                indexes.push(i)
            }
            dstr = e.Date.toString().toLowerCase()
            if(dstr.includes(sstr) && !(indexes.includes(i))){
                indexes.push(i)
            }
            dstr = e.active.toString().toLowerCase()
            if(dstr.includes(sstr) && !(indexes.includes(i))){
                indexes.push(i)
            }
        });
        var sdata = []
        indexes.forEach((i) =>{
            sdata.push(full_data[i])
        })
        data=JSON.parse(JSON.stringify(sdata))
    }
    scr_out()
}


;(function(){
    $(search_box).bind("keyup paste", function (e) {
        search(this.value)
    });
})()