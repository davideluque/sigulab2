var table = $('#datatable').DataTable({
"dom": "<'row buscar'<'col-md-3'f>>"+"<'row'<'col-md-8'l><'col-md-4'i>>"+"<'row'rt>"+"<'row'<'col-md-12'p>>",
language: {
  url: langDT
},
initComplete: function(){
  var api = this.api();

  new $.fn.dataTable.Buttons(api, {
     buttons: [
       {
          text:'<i class="fa fa-filter"></i>',
          action: function(){
            mostrarFiltro()
          },
          className: 'boton-sigulab'
       },
       {
         extend: 'collection',
         text: '<i class="fa fa-save"></i>',
         className: 'boton-sigulab dropDown',
         background:false,
         fade:true,
         buttons:[
            {extend:'copy', text:"Copiar"},
             'pdf',
             'excel'
         ]
       },
       { 
         extend:'print',
        text: '<i class="fa fa-print"></i>'
       }
     ]
  });
  api.buttons().container().appendTo('#buttons');
$('#datatable_previous').html('<span class="fa fa-arrow-left" title="Anterior"/>');
  $('#datatable_next').html('<span class="fa fa-arrow-right" title="Siguiente"/>');
  $('#buttons').style.textAlign = "right";

  
  
}

});
var w2p_ajax_confirm_message =
        "{{=T('')}}";

window.onclick = function(event) {
  if (!event.target.matches('.dropDown')) {
    $(".dt-button-collection").hide();
  }
}
        
      
