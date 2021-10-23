function Editar() {
    const contenedormodal = document.getElementById('contenedor-editar');
    const editar = document.getElementsByClassName('editar');
    const cancelar = document.getElementById('boton-cancelaredit');

   /*  editar.addEventListener('click', () => {
        contenedormodal.classList.add('showeditar');

    }) */
    for (var i=0; i< editar.length; i++) {
        //Añades un evento a cada elemento
        editar[i].addEventListener("onmouseover",function() {
           //Aquí la función que se ejecutará cuando se dispare el evento
           contenedormodal.classList.add('showeditar'); //En este caso alertaremos el texto del cliqueado
           
        });
    }

    cancelar.addEventListener('click', () => {
        contenedormodal.classList.remove('showeditar');
    })

}

const contenedormodal = document.getElementById('contenedor-editar');
const editar = document.getElementsByClassName('editar');
const contenedormodaldash = document.getElementById('contenedor-ed');
const cancelar = document.getElementById('boton-cancelaredit');

function MostrarEdit(){
    contenedormodal.classList.add('showeditar');
    
}

function MostrarEditdash(){
    contenedormodaldash.classList.add('showeditar');
}

function retirardash(){
    contenedormodaldash.classList.remove('showeditar');
}
function retirar(){
    contenedormodal.classList.remove('showeditar');
}



function Guardar() {
    const contenedormodal = document.getElementById('contenedor-nuevo');
    const editar = document.getElementsByClassName('boton-nuevo');
    const cancelar = document.getElementById('boton-cancelarnuevo');

   /*  editar.addEventListener('click', () => {
        contenedormodal.classList.add('showeditar');

    }) */
    for (var i=0; i< editar.length; i++) {
        //Añades un evento a cada elemento
        editar[i].addEventListener("click",function() {
           //Aquí la función que se ejecutará cuando se dispare el evento
           contenedormodal.classList.add('showeditar'); //En este caso alertaremos el texto del cliqueado
           
        });
    }

    cancelar.addEventListener('click', () => {
        contenedormodal.classList.remove('showeditar');
    })
}


function Eliminar() {
    const contenedormodal = document.getElementById('contenedor-eliminar');
    const eliminar = document.getElementsByClassName('eliminar');
    const cancelar = document.getElementById('boton-cancelardelete');

    for (var i=0; i< eliminar.length; i++) {
        //Añades un evento a cada elemento
        eliminar[i].addEventListener("click",function() {
           //Aquí la función que se ejecutará cuando se dispare el evento
           contenedormodal.classList.add('showeliminar'); //En este caso alertaremos el texto del cliqueado
        });
    }

    cancelar.addEventListener('click', () => {
        contenedormodal.classList.remove('showeliminar');
    })
}
/* 
$('#search').on('keyup',function(){
    var value = $(this).val()
    console.log('value', value)
    table = document.getElementById("tabla");
    
    console.log(table.length)
    for (i = 0; i < table.length; i++) {
        reg = table[i].getElementsByTagName("tr")
        console.log(reg)
    }
})
 */

$(document).ready(function() {
    $('#tabla').DataTable();
} );




/* document.addEventListener('mousedown', function(evt) {
    evt.preventDefault();
    return false;
  });
  // BONUS - Deshabilitamos el menu contextual
  document.addEventListener('contextmenu', function(evt) {
    evt.preventDefault();
    return false;
  });
 */


