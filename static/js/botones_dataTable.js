var table = $('#datatable1').DataTable({
"dom": "<'row buscar1'f>"+"<'row'<'col-md-6'l><'col-md-6'i>>"+"<'row'rt>"+"<'row'<'col-md-12'p>>",
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
            mostrarFiltro1()
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
         extend:'',
        text: '<i class="fa fa-print" onclick="generarPDF() "></i>'
       }
     ]
  });
  api.buttons().container().appendTo('.buscar1');
  $('#datatable1_previous').html('<span class="fa fa-arrow-left"/>');
  $('#datatable1_next').html('<span class="fa fa-arrow-right" />');
  
  
}
});

var table1 = $('#datatable2').DataTable({
  "dom": "<'row buscar2'f>"+"<'row'<'col-md-6'l><'col-md-6'i>>"+"<'row'rt>"+"<'row'<'col-md-12'p>>",
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
              mostrarFiltro2()
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
    api.buttons().container().appendTo('.buscar2');
    $('#datatable2_previous').html('<span class="fa fa-arrow-left"/>');
    $('#datatable2_next').html('<span class="fa fa-arrow-right" />');
    
    
  }


});

var w2p_ajax_confirm_message =
        "{{=T('')}}";

window.onclick = function(event) {
  if (!event.target.matches('.dropDown')) {
    $(".dt-button-collection").hide();
  }
  $('#datatable1_previous').html('<span class="fa fa-arrow-left"/>');
  $('#datatable1_next').html('<span class="fa fa-arrow-right" />');
  $('#datatable2_previous').html('<span class="fa fa-arrow-left"/>');
  $('#datatable2_next').html('<span class="fa fa-arrow-right" />');
}
        
      
