const all_seats=document.querySelectorAll('.row .seat')
const cta_btn=document.querySelector('button.purchase_btn')

async function contactAPI(url,body){
    const response=await fetch(url,{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify(body)
    })

    return response.json()
}


function refreshSeat(){
    const trips=movieSelect.options[movieSelect.selectedIndex].id

    contactAPI("/occupied/",{trips}).then(data=>{
        const occupied_seat=data['occupied_seats']
        const trips=data["trip"]

        const seat_LocalStorage=localStorage.getItem('selectedSeats')?JSON.parse(localStorage.getItem('selectedSeats')):null
        const movie_index=localStorage.getItem("selectedMovieIndex")

        all_seats.forEach(seat=>{
            seat.classList.remove("occupied")
        })


        const LS_movie=movieSelect.options[movie_index].textContent

        if (LS_movie===trips){
            if (occupied_seat !== null && occupied_seat.length > 0){
                all_seats.forEach((seat,index)=>{
                    if(occupied_seat.indexOf(index) > -1){
                        seat.classList.add('occupied')
                        seat.classList.remove('selected')
                    }
                })
            }

            if(seat_LocalStorage !== null){
                seat_LocalStorage.forEach((seat,index)=>{
                    if (occupied_seat.includes(seat)){
                        seat_LocalStorage.splice(index,1)
                        localStorage.setItem("selectedSeats",seat_LocalStorage)
                    }
                })
            }
        }
        updateSelectedCount()
    })
}
refreshSeat()


cta_btn.addEventListener("click",e=>{
    const trip_name=movieSelect.options[movieSelect.selectedIndex].id
    const seat_list=JSON.parse(localStorage.getItem("selectedSeats"))

    if(seat_list !== null && seat_list.length > 0){
        data={
            trip_name,
            seat_list
        }
    }
    contactAPI("/payment/",data).then(
    location.href = "/confirm")
})

