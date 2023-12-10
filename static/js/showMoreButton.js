const number = 3;

let w = document.querySelectorAll(".content-wrapper");
    for (let i = 0; i < w.length; i++) {
        let c = w[i].querySelectorAll(".content");
        $(c).slice(0,number).show();
        if(c.length <= number){
            noMoreContentButton(w[i].querySelector(".show-more"));
        }
    }

    function noMoreContentButton(button){
        button.innerHTML = "Mais nada para mostrar";
        button.classList = "show-more noContent";
    }

    function showMoreContent(button){
        let contentWrapper = button.parentNode.parentNode;
        let contents = $(contentWrapper).find('.content:hidden');
        contents.slice(0, number).slideDown();
        if(contents.length <= number){
            noMoreContentButton(button);
        }
    }