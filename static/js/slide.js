function mostrar(){
    const btn = document.querySelector('#menubt');
    const menu = document.querySelector('#contenedorderecha');

    btn.addEventListener('click', function () {
        menu.classList.toggle("collapsed");
        menu.classList.toggle("expanded");
    });
}
