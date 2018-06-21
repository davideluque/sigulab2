var table = $('#datatable').DataTable({
"dom": "<'row buscar'<'col-md-1'f>>"+"<'row'<'col-md-8'l><'col-md-4'i>>"+"<'row'rt>"+"<'row'<'col-md-12'p>>",
language: {
  url: langDT
},
initComplete: function(){
  var api = this.api();

  new $.fn.dataTable.Buttons(api, {
     buttons: [
         {extend:'copy', text:"Copiar"}, 'pdf', 'excel', 'print'
     ]
  });
  api.buttons().container().appendTo('#buttons');
  $('.buttons-pdf').html('<span class="glyphicon glyphicon-file" data-toggle="tooltip" title="Export To PDF"/>');
  $('.buttons-print').html('<span class="glyphicon glyphicon-print" data-toggle="tooltip" title="Print"/>');
  $('.buttons-copy').html('<span class="glyphicon glyphicon-copy" data-toggle="tooltip" title="Copy"/>');
  $('.buttons-excel').html('<span class="glyphicon glyphicon-floppy-disk" data-toggle="tooltip" title="Copy"/>');
  $('#datatable_previous').html('<span class="fa fa-arrow-left" title="Anterior"/>');
  $('#datatable_next').html('<span class="fa fa-arrow-right" title="Siguiente"/>');
  $('#buttons').style.textAlign = "right";
  
}

});
var w2p_ajax_confirm_message =
        "{{=T('')}}";
