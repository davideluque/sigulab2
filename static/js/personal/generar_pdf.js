// Script que se encarga de la generacion de pdfs del modulo 
// de personal
function generarPDF(){
    const container = document.getElementById('imprimir_listado')
    const table = $('#datatable1').DataTable()
    $('#datatabla tbody').html('')
    table.rows({filter: 'applied'}).data().toArray()
        .filter(l => l[0])
        .map(l => $(l[0]))
        .map(l => `
            <tr>
                <td class="casillas-pdf">${l.data('nombre')} ${l.data('apellido')}</td>
                <td class="casillas-pdf">${l.data('unidad_jerarquica_superior')}</td>
                <td class="casillas-pdf">${l.data('email')}</td>
                <td class="casillas-pdf">${l.data('gremio')}</td>
                <td class="casillas-pdf">${moment().year() - moment(l.data('fecha-ingreso')).year()}</td>
            </tr>`)
        .forEach(a => {
            $('#datatabla tbody').append(a)
        })
    html2pdf(document.getElementById('imprimir_listado'));
    $.ajax({
        method: 'POST',
        url: url,
        data: {'a': 'a'},
        success: function() {},
        fail: function() {}
    })
}