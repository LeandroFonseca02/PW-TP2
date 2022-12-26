function changeInputs(button){
    let form = button.parentNode.parentNode.parentNode.parentNode.parentNode.querySelector("form");
    let origem = form.querySelector(".inputOrigem");
    let destino = form.querySelector(".inputDestino");
    if(button.classList.contains("inputDestino")){
        origem.value = "";
        destino.value = "ISMAT";
        destino.readOnly = true;
        origem.readOnly = false;
    }else{
        destino.value= "";
        origem.value = "ISMAT";
        origem.readOnly = true;
        destino.readOnly = false;
    }
    $(button).toggleClass('active')
        .siblings().not(this).removeClass('active');
}
