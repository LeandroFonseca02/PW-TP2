function getUserModal(user_id){
    modalWrapper = document.getElementById("modalsProfile");
    fetch('/getProfileModal/'+user_id, {
        method: "GET"
    }).then(response => {
        return response.text();
    }).then(html => {
        modalWrapper.innerHTML = html;
        $.getJSON('/getUserRating/'+user_id, function (response) {
            ratingElement = document.querySelector('#profileCardAvaliacao'+user_id);
            starRatingGenerator(ratingElement,response.rating);
        })
        $("#profileCard"+user_id).modal("toggle");
    });
}

function reservation(ride_id){
    fetch('/reservation/'+ride_id, {
        method:"POST",
        headers:{'Content-Type': 'application/json'},
        body:JSON.stringify({ride_id:ride_id})
    })
}

function createStar(div,score){
    let star;
    if(score >= 0 && score < 0.5){
        star = "star";
    }else if(score >= 0.5 && score < 1){
        star = "star-half";
    }else if(score === 1){
        star = "star-fill";
    }
    let img = document.createElement("img");
    img.src="../static/images/icons/" + star + ".svg";
    img.alt=star;
    img.style.height = "28px";
    div.appendChild(img);
}

function getStarScore(rating){
    let array = [];
    let a = rating;
    for (let i = 0; i < 5; i++) {
        if (a>=1){
            array.push(1);
        }else if (a>=0.5 && a<1){
            array.push(a);
        }else if (a>=0 && a<0.5){
            array.push(a);
        }else {
            array.push(0);
        }
        a--;
    }
    return array;
}

function starRatingGenerator(element,rating){
    let div = document.createElement('div');
    element.appendChild(div)
    let array = getStarScore(rating);
    for (let i = 0; i < 5; i++) {
        createStar(div,array[i]);
    }

}

function changeExpandIcon(element) {
    let img = element.querySelector("img");
    cardContent = document.getElementById("cardContent"+element.name);


    fetch('/getRideData/'+element.name, {
        method: "GET"
    }).then(response => {
        return response.text();
    }).then(html => {
        img.src = (img.src.includes('icon-down.svg')) ? '../static/images/icons/icon-up.svg' : '../static/images/icons/icon-down.svg';
        cardContent.innerHTML = html;
        $.getJSON('/getRideRating/'+element.name, function (response) {
            condutor = cardContent.querySelector('#cardContentAvaliacao'+response.ride_id + response.condutor_id);
            passengers = response.passengers;
            starRatingGenerator(condutor,response.condutor_classification)
            for (let i = 0; i < passengers.length; i++) {
                let el = cardContent.querySelector('#cardContentAvaliacao'+response.ride_id + passengers[i].passenger_id)
                starRatingGenerator(el, passengers[i].passenger_classification)
            }
        })

        $('#cardContent'+element.name).collapse('toggle')
    });
}

function debugStarRating(){
    let rating = document.querySelectorAll(".rating-wrapper")
    for (let i = 0; i < rating.length; i++) {
        let inputs = rating[i].querySelectorAll("input");
        for (let j = 0; j < inputs.length; j++) {
            if (inputs[j].checked === true){
                console.log("Rating " + (i+1) + ": valor " + inputs[j].value)
            }
        }
    }
}
function createStarRating(element,number){
    const div = document.createElement("div");
    div.className = "rating-wrapper";
    for (let i = 0; i < 5; i++) {
        let input = document.createElement("input");
        input.type = "radio";
        input.name = "star-rating"+number;
        input.id = input.name+"-"+i;
        input.value = 5-i;
        let label = document.createElement("label");
        label.htmlFor = input.id;
        let star = document.createElement("i");
        star.classList = "fas fa-star d-inline-block";
        div.appendChild(input);
        div.appendChild(label)
        label.appendChild(star);
    }
    element.appendChild(div);
    element.appendChild(document.createElement("br"));
}

function createProfileModal(cardId,passengerID,user,parentDiv,id){
    let modal = `<div class="modal fade" id="${"profileCard" + id +cardId+"-"+passengerID}"
        data-bs-keyboard="false" tabindex="-1"
        aria-labelledby="${"profileCardLabel" + id +cardId+"-"+passengerID}"
        aria-hidden="true">
            <div class="modal-dialog">
                  <div class="modal-content">
                      <div class="modal-header">
                          <h5 class="modal-title" id="${"profileCardTitle" + id +cardId+"-"+passengerID}">Perfil</h5>
                          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                      </div>
                      <div class="modal-body">
                          <div class="col d-flex flex-column">
                              <div class="col mb-3">
                                  <div class="col d-flex flex-column  align-items-center bg-light perfil-caixa justify-content-center h-100">
                                      <div class="col d-flex flex-column justify-content-center align-items-center justify-content-center mt-2">
                                          <div class="mt-2">
                                              <img src="${user.photo}" alt="mdo" class="rounded-circle profile-image">
                                          </div>
                                      </div>
                                      <div class="d-flex mb-3">
                                          <h5>${user.firstName + " " + user.lastName}</h5>
                                      </div>

                                  </div>
                              </div>

                              <div class="col mb-3">
                                  <div class="col d-flex flex-column  align-items-center bg-light perfil-caixa justify-content-center h-100">
                                      <h5 class="mt-2">Avaliação:</h5>
                                      <div class="mt-2 mb-2" id="${"profileCardAvaliacao" + id +cardId+"-"+passengerID}"></div>
                                  </div>
                              </div>

                              <div class="col d-flex flex-column bg-light perfil-caixa">
                                  <div class="mt-2 mb-3 ms-2">
                                      <h5>Dados Pessoais</h5>
                                  </div>
                                  <div class="col d-flex flex-column justify-content-center mb-1">
                                      <div class="row g-3 ms-1">
                                          <div class="col-8">
                                              <label>Endereço de email</label>
                                              <h5>${user.email}</h5>
                                          </div>
                                          <div class="col-4">
                                              <label>Telemóvel</label>
                                              <h5>${user.phoneNumber}</h5>
                                          </div>
                                      </div>
                                  </div>
                              </div>
                          </div>
                      </div>
                  </div>
              </div>
            </div>`;

    parentDiv.innerHTML += modal;
    let avaliacao = document.getElementById("profileCardAvaliacao" + id +cardId+"-"+passengerID);
    starRatingGenerator(avaliacao,user.rating);
}

function createCard(idCard, data, parentDiv, id) {
    let passengers = data.passengers;
    let card = `
        <div class="content">
        <div class="card boleia-card boleia-card-shadow mt-3">
            <div class="card-body">
                <div class="d-flex flex-row boleia-header align-items-center gap-4">
                    <img class="ms-4 d-lg-block d-md-none car-card-image" src="./images/car-placeholder.png" alt="Car">
                    <div class="col">
                        <div class="align-self-start card-header-text">${data.origem} - ${data.destino}</div>                       
                    </div>
                    <div class="col card-header-text">${data.status}</div>
                    <div class="card-header-text">${data.date}</div>
                    <div class="card-header-text"> ${data.hour}</div>
                    <div>
                        <button class="btn" type="button" data-bs-toggle="collapse" data-bs-target=${"#cardContent" + id + idCard}
                                aria-expanded="false" aria-controls=${"#cardContent" + id + idCard}
                                onclick="changeExpandIcon(this)">
                            <img src="./images/icons/icon-down.svg" style="height: 24px" alt="expandir">
                        </button>
                    </div>
                </div>
    
                <div id=${"modals" + id + idCard}></div>
            </div>
    
    
            <div class="collapse" id="${"cardContent" + id + idCard}">
                <div class="card-blocker"></div>
                <div class="row">
                    <div class="col-xl-6 col-lg-12 col-md-12 col-sm-12 col-xs-12">
                        <div class="table-responsive text-nowrap">
                            <table class="text-nowrap w-auto">
                                <tbody>
                                ${passengers.map((user,index) =>
        `
                                    <tr id="${"Passenger" + id +index + "-" + idCard}" class="table-row">
                                        <td>
                                            <a href="" data-bs-toggle="modal" data-bs-target="${"#profileCard" + id +idCard+"-"+ index}">
                                                <img class="ms-4 p-2 me-2 rounded-circle card-profile-image" src="${user.photo}"
                                                     alt="Profile Image">
                                            </a>
                                        </td>
                                        <td class="ps-3">${user.firstName}</td>
                                        <td>
                                            <div class="ms-3" id="${"cardContentAvaliacao" + id +idCard+index}"></div>
                                        </td>
                                        <td>
                                            <div id="${"cardContentRemove" + id +idCard+index}"></div>
                                        </td>
                                    </tr>`).join('')}
                                </tbody>
                            </table>
                        </div>
                    </div>
    
                    <div class="col-xl-5 col-lg-12 col-md-12 col-sm-12 col-xs-12">
                        <div class="card m-3">
                            <div class="card-header">
                                Descrição
                            </div>
                            <div class="card-body">
                                <p>Veículo:<br>
                                    &emsp; Marca: ${data.vehicle.marca}<br>
                                    &emsp; Modelo: ${data.vehicle.modelo}<br>
                                    &emsp; Cor: ${data.vehicle.cor}<br>
                                    &emsp; Matrícula: ${data.vehicle.matricula}<br>
                                    Preço: ${data.pricePerPassenger}<br>
                                    ${data.description}
                                    </p>
                            </div>
                        </div>
                        <div class="mt-3 px-1 m-3">
                            <p>Lugares Disponíveis: ${data.nrLugaresDisponiveis - data.passengers.length}</p>
                        </div>
                    </div>
    
                </div>
                <div class="card-blocker"></div>
                <div class="d-flex flex-row-reverse">
                    <div class="me-4" id="${"cardContentButtons" + id  + idCard}">
                    </div>
                </div>
                <div class="card-blocker"></div>
            </div>
        </div>
    </div>`;

    parentDiv.innerHTML += card;
    let string = "#cardContentAvaliacao" + id  + idCard;
    let modals = "#modals" + id  + idCard
    for (let i = 0; i < passengers.length; i++) {
        let avaliacao = document.querySelector(string+i);
        starRatingGenerator(avaliacao,passengers[i].rating);
        createProfileModal(idCard,i,passengers[i],document.querySelector(modals),id);
    }
}

function createCardGenerico(idCard, data, parentDiv, id) {
    createCard(idCard,data,parentDiv,id);
    let buttonWrapper = document.getElementById("cardContentButtons"+id+idCard);
    let reservar = `<button type="button" class="btn-ismat-large" data-bs-toggle="modal" data-bs-target="${"#reservationBoleia"+id+idCard}">Reservar</button>`;
    buttonWrapper.innerHTML += reservar;
    createReservationModal(idCard,data,parentDiv,id);
}

function createCardReservaAtiva(idCard, data, parentDiv,id) {
    createCard(idCard,data,parentDiv,id);
    let buttonWrapper = document.getElementById("cardContentButtons"+id+idCard);
    let cancelar = `<button type="button" class="btn-ismat-large" data-bs-toggle="modal" data-bs-target="${"#cancelReserva"+id+idCard}">Cancelar</button>`;
    buttonWrapper.innerHTML += cancelar;
    createCancelReservaModal(idCard,data,buttonWrapper,id);
}

function createProfile(user) {
    document.querySelector("#profileName").innerText = user.firstName + " " + user.lastName;
    document.querySelector("#profileImage").src = user.photo;
    starRatingGenerator(document.getElementById("profileRating"),user.rating);
    document.querySelector("#floatingEmail").value = user.email;
    document.querySelector("#floatingPhoneNumber").value = user.phoneNumber;
    document.querySelector("#floatingFirstName").value = user.firstName;
    document.querySelector("#floatinglastName").value = user.lastName;
    document.querySelector("#headerProfile").src = user.photo;
}

function getVehiclesOnSelector(selector, data) {
    for (let i = 0; i < vehicles.length; i++) {
        selector.innerHTML += `<option value="${i+1}">${data[i].marca + " " + data[i].modelo + " (" + data[i].matricula + ")"}</option>`
    }
}

function createListOfCards(element,data,type){
    type = (type === undefined) ? 0 : type;
    switch (type) {
        case 0:
            for (let i = 0; i < data.length; i++) {
                createCardGenerico(i,data[i],element,"Generico");
            }
            break;
        case 1:
            for (let i = 0; i < data.length; i++) {
                createBoleiaAtiva(i,data[i],element,"BoleiaAtiva");
            }
            break;
        case 2:
            for (let i = 0; i < data.length; i++) {
                createCard(i,data[i],element,"BoleiaHistorico");
            }
            break;
        case 3:
            for (let i = 0; i < data.length; i++) {
                createCardReservaAtiva(i,data[i],element,"ReservaAtiva");
            }
            break;
        case 4:
            for (let i = 0; i < data.length; i++) {
                createCard(i,data[i],element,"ReservaHistorico");
            }
            break;
    }

}

function generateRatings(data,parentDiv) {
    for (let i = 0; i < data.length; i++) {
        let rating =
            `<tr>
              <td>
                <img class="ms-4 p-2 card-profile-image rounded-circle" src="${data[i].photo}"
                    alt="Profile Image">
              </td>
              <td class="ps-3">${data[i].firstName}</td>
              <td>
                <div id="${"rating"+i}">
                </div>
              </td>
              <div id="${"ratingProfileModal"+i}"></div>
            </tr>`;
        parentDiv.innerHTML += rating;
        let id = "#rating" + i;
        createStarRating(parentDiv.querySelector(id),i);
    }
}

function createReservationModal(idCard,data,parentDiv,id) {
    let modal =
        `<div class="modal fade" id="${"reservationBoleia"+id+idCard}"
            data-bs-keyboard="false" tabindex="-1"
            aria-labelledby="${"reservationBoleiaLabel"+id+idCard}"
            aria-hidden="true">
            
            <div class="modal-dialog">
              <div class="modal-content">
                <div class="modal-header">
                  <h5 class="modal-title" id="${"reservationBoleiaTitle"+id+idCard}">Reservar Boleia</h5>
                  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                  <p>Tem a certeza que quer reservar a boleia ${data.origem + "-" + data.destino}?</p>
                </div>
                <div class="modal-footer">
                  <button type="button" class="btn btn-success" data-bs-dismiss="modal">Sim</button>
                  <button type="button" class="btn btn-danger" data-bs-dismiss="modal">Não</button>
                </div>
              </div>
            </div>
        </div>`;
    parentDiv.innerHTML +=modal;
}

function createConfirmationModal(idCard,data,parentDiv,id) {
    let modal =
        `<div class="modal fade" id="${"confirmationBoleia"+id+idCard}"
            data-bs-keyboard="false" tabindex="-1"
            aria-labelledby="${"confirmationBoleiaLabel"+id+idCard}"
            aria-hidden="true">
            
            <div class="modal-dialog">
              <div class="modal-content">
                <div class="modal-header">
                  <h5 class="modal-title" id="${"confirmationBoleiaTitle"+id+idCard}">Confirmar Boleia</h5>
                  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                  <p>Tem a certeza que quer confirmar a boleia ${data.origem + "-" + data.destino}?</p>
                </div>
                <div class="modal-footer">
                  <button type="button" class="btn btn-success" data-bs-dismiss="modal">Sim</button>
                  <button type="button" class="btn btn-danger" data-bs-dismiss="modal">Não</button>
                </div>
              </div>
            </div>
        </div>`;
    parentDiv.innerHTML +=modal;
}

function createCancelBoleiaModal(idCard,data,parentDiv,id) {
    let modal =
        `<div class="modal fade" id="${"cancelBoleia"+id+idCard}"
            data-bs-keyboard="false" tabindex="-1"
            aria-labelledby="${"cancelBoleiaLabel"+id+idCard}"
            aria-hidden="true">
            
            <div class="modal-dialog">
              <div class="modal-content">
                <div class="modal-header">
                  <h5 class="modal-title" id="${"cancelBoleiaTitle"+id+idCard}">Cancelar Boleia</h5>
                  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                  <p>Tem a certeza que quer cancelar a boleia ${data.origem + "-" + data.destino}?</p>
                </div>
                <div class="modal-footer">
                  <button type="button" class="btn btn-success" data-bs-dismiss="modal">Sim</button>
                  <button type="button" class="btn btn-danger" data-bs-dismiss="modal">Não</button>
                </div>
              </div>
            </div>
        </div>`;
    parentDiv.innerHTML +=modal;
}

function createCancelReservaModal(idCard,data,parentDiv,id) {
    let modal =
        `<div class="modal fade" id="${"cancelReserva"+id+idCard}"
            data-bs-keyboard="false" tabindex="-1"
            aria-labelledby="${"cancelReservaLabel"+id+idCard}"
            aria-hidden="true">
            
            <div class="modal-dialog">
              <div class="modal-content">
                <div class="modal-header">
                  <h5 class="modal-title" id="${"cancelReservaTitle"+id+idCard}">Cancelar Reserva</h5>
                  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                  <p>Tem a certeza que quer cancelar a reserva ${data.origem + "-" + data.destino}?</p>
                </div>
                <div class="modal-footer">
                  <button type="button" class="btn btn-success" data-bs-dismiss="modal">Sim</button>
                  <button type="button" class="btn btn-danger" data-bs-dismiss="modal">Não</button>
                </div>
              </div>
            </div>
        </div>`;
    parentDiv.innerHTML +=modal;
}

function createKickingModal(idCard,passengerID,user,parentDiv,id) {
    let modal =
        `<div class="modal fade" id="${"expulsarPassenger"+id+passengerID+"-"+idCard}"
            data-bs-keyboard="false" tabindex="-1"
            aria-labelledby="${"expulsarPassengerLabel"+id+passengerID+"-"+idCard}"
            aria-hidden="true">
            
            <div class="modal-dialog">
              <div class="modal-content">
                <div class="modal-header">
                  <h5 class="modal-title" id="${"expulsarTitle"+id+passengerID+"-"+idCard}">Expulsar Passageiro</h5>
                  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                  <p>Tem a certeza que quer expulsar ${user.firstName + " " + user.lastName} da sua boleia?</p>
                </div>
                <div class="modal-footer">
                  <button type="button" class="btn btn-success" data-bs-dismiss="modal">Sim</button>
                  <button type="button" class="btn btn-danger" data-bs-dismiss="modal">Não</button>
                </div>
              </div>
            </div>
        </div>`;
    parentDiv.innerHTML +=modal;
}

function createBoleiaAtiva(idCard, data, parentDiv,id) {
    createCard(idCard,data,parentDiv,id);
    let card = document.getElementById("cardContent"+id+idCard);
    let passengers = card.querySelectorAll(".table-row");

    for (let i = 1; i < passengers.length; i++) {
        passengers[i].innerHTML += `
        <td>
            <div id="${"expulsarPassengerModal"+id+i+"-"+idCard}"></div>
            <button type="button" class="btn-ismat-close ms-3" data-bs-toggle="modal" data-bs-target="${"#expulsarPassenger"+id+i+"-"+idCard}">
                <i class="fas fa-times-circle" style="font-size: 24px"></i>
            </button>
        </td>`;
        createKickingModal(idCard,i,data.passengers[i],document.getElementById("expulsarPassengerModal"+id+i+"-"+idCard),id);
    }
    let buttonWrapper = document.getElementById("cardContentButtons"+id+idCard);
    let confirmBtn = `<button type="button" class="btn-ismat-large me-3" data-bs-toggle="modal" data-bs-target="${"#confirmationBoleia"+id+idCard}">Confirmar</button>`;
    let cancelBtn = `<button type="button" class="btn-ismat-large" data-bs-toggle="modal" data-bs-target="${"#cancelBoleia"+id+idCard}">Cancelar</button>`;
    buttonWrapper.innerHTML = confirmBtn;
    buttonWrapper.innerHTML += cancelBtn;
    createConfirmationModal(idCard,data,buttonWrapper,id);
    createCancelBoleiaModal(idCard,data,buttonWrapper,id);
}

function createCarsManager(vehicles, element) {
    for (let i = 0; i < vehicles.length; i++) {
        let car =
            `<div class="d-flex align-items-start perfil-caixa bg-light mb-2" id="${"carManager"+i}">
                <img class="ms-4 d-none d-md-block me-4 align-self-center" src="/images/car-placeholder.png" alt="Car" style="height: 100px">
                <div>
                    <div>
                        <div class="">Matrícula: ${vehicles[i].matricula}</div>
                        <div class="">Marca: ${vehicles[i].marca}</div>
                        <div class="">Modelo: ${vehicles[i].modelo}</div>
                        <div class="">Cor: ${vehicles[i].cor}</div>
                    </div>
                </div>
                <div class="d-flex col flex-column">
                    <button type="button" class="btn-close align-self-end me-2 mt-1" aria-label="Delete"></button>
                </div>
            </div>`;
        element.innerHTML += car;
    }
}