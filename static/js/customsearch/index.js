'use strict';

var baseUrl = document.location.href;
// urls busquedas
var queryUrl = 'search/';

// urls exportar reportes
var exportUrl = 'reports/export/';

// urls para modal detalle de email
var emailDetailUrl = 'email-detail/';

// url link storage
var attachUrl = 'https://storage.googleapis.com';

// link dinamico para las rutas de exportar
var exportLink = '';

// expresión regular de correo
var expr = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,4})+$/;

$( document ).ready( function () {
	baseUrl = baseUrl.split('/');
	delete baseUrl[4];
	delete baseUrl[3];
	baseUrl = baseUrl.join('/')
	baseUrl = baseUrl.substring( 0, baseUrl.length - 1 );
	
	$( '.datePicker' ).datetimepicker ({
		'dayOfWeekStart': 1,
		'lang': 'es',
		'timepicker': false,
		'format': 'd/m/Y',
		'formatDate': 'Y/m/d',
	});

	setDefaultDates();
	$( '#menuModal' ).modal( 'show', true );
	
});

$( '#run_search' ).on( 'click', function () {

	// validar campos en formulario
	if ( !formValidate() ) {
		$( '#errorModal' ).modal( 'show', true );
		console.log("aqui llego");
		return;
	};

	$( '#closeMenuModal' ).click();
	$( '#loadingModal' ).modal( 'show', true );
	
	// toma de valores de los parámetros
	var date_from = $( '#date_from' ).val();
	var date_to = $( '#date_to' ).val();
	var correo = $( '#correoDestinatario' ).val();
	var empresas = $( '#empresas' ).val();
	var numeroFolio = $( '#numeroFolio' ).val();
	var rutReceptor = $( '#rutReceptor' ).val();
	var mount_from = $( '#mount_from' ).val();
	var mount_to = $( '#mount_to' ).val();
	var checkFallidos = $( '#checkFallidos' ).is( ':checked' );

	if ( rutReceptor && !validaRut( rutReceptor ) ) {
		$( '#closeLoadingModal' ).click();
		return;
	} else {
		rutReceptor = '-';
	};

	date_from = getDateAsTimestamp( date_from );
	date_to = getDateAsTimestamp( date_to );

	if ( mount_from && mount_to ) {
		mount_from = parseInt( mount_from, 10 );
		mount_to = parseInt( mount_to, 10 );
	} else {
		mount_from = '-';
		mount_to = '-';
	};

	if ( correo ) {
		correo = encodeURIComponent( correo );
	} else {
		correo = '-';
	};

	if ( !numeroFolio ) {
		numeroFolio = '-';
	};

	var link = queryUrl + date_from + '/' + date_to + '/' + empresas + '/' + correo + '/';
	link += numeroFolio + '/' + rutReceptor + '/' + mount_from + '/' + mount_to + '/' + checkFallidos + '/';

	$( '#closeLoadingModal' ).click();
	drawJqueryTable( link );

	exportLink = baseUrl + exportUrl + date_from + '/' + date_to + '/' + empresas + '/' + correo + '/';
	exportLink += numeroFolio + '/' + rutReceptor + '/' + mount_from + '/' + mount_to + '/' + checkFallidos + '/';
	$( '#btnGenerateReport' ).show();
});

$( '#btnGenerateReport' ).on( 'click', function () {
	var btn = $( this );
	btn.removeClass( 'mdi-content-send' );
	btn.addClass( 'mdi-action-cached' );
	btn.attr( 'disabled', true );
	sendUrlToReportQueue ( exportLink, btn );
	var title = "Reporte Tracking";
	var body = "Se ha iniciado el proceso de generar un reporte Excel ";
	body += "cuando este proceso finalice recibirás un email con el archivo adjunto, ";
	body += "por favor espere unos minutos...";
	notificationModal ( title, body );
});

function notificationModal ( t, b ) {
	var title = $( '#notificationTitle' );
	var body = $( '#notificationBody' );
	title.empty().append( t );
	body.empty().append( b );
	$( '#notificationModal' ).modal( 'show', true );
};

function sendUrlToReportQueue ( link, btn ) {
	$.ajax({
		url: link,
		type: 'GET',
		dataType: 'json',
		success: function ( data ) {
			btn.removeClass( 'mdi-action-cached' );
			btn.addClass( 'mdi-content-send' );
			btn.attr( 'disabled', false );
			console.log( data );
		},
		error: function ( jqXHR, textStatus, errorThrown ) {
			btn.removeClass( 'mdi-action-cached' );
			btn.addClass( 'mdi-content-send' );
			btn.attr( 'disabled', false );
			console.log( errorThrown );
		},
	});
};

function formValidate () {

	var date_from = $( '#date_from' ).val();
	var date_to = $( '#date_to' ).val();
	var correoDestinatario = $( '#correoDestinatario' ).val();
	var empresas = $( '#empresas' ).val();
	var mount_from = $( '#mount_from' ).val();
	var mount_to = $( '#mount_to' ).val();
	var numeroFolio = $( '#numeroFolio' ).val();
	var rutReceptor = $( '#rutReceptor' ).val();
	var checkFallidos = $( '#checkFallidos' ).is( ':checked' );

	if ( date_from && date_to ) {
		return true;
	} else {
		return false;
	};

	if ( correoDestinatario && expr.test( correoDestinatario ) ) {
		return true;
	} else {
		return false;
	};

	return true;

};

function clearForm () {
	$( '#correoDestinatario' ).val( '' );
	$( '#mount_from' ).val( '' );
	$( '#mount_to' ).val( '' );
	$( '#numeroFolio' ).val( '' );
	$( '#rutReceptor' ).val( '' );
	setDefaultDates();
};

$( '#showMenu' ).on( 'click', function () {
	$( '#menuModal' ).modal( 'show', true );
});

$( '.datePicker' ).on( 'change', function () {
	var date_from = $( '#date_from' ).val();
	var date_to = $( '#date_to' ).val();

	date_from = moment( date_from, 'DD/MM/YYYY' ).unix();
	date_to = moment( date_to, 'DD/MM/YYYY' ).unix();

	if ( date_from > date_to ) {
		setDefaultDates();
	};
});

$( '.nav-pills' ).on('click', 'a', function () {

	tabPosition = $( this ).attr( 'href' );

});

// Validar los campos de fecha
$( '.datePicker' ).on( 'change', function () {

	var date_from = $( '#date_from' ).val();
	var date_to = $( '#date_to' ).val();

	date_from = moment( date_from, 'DD/MM/YYYY' ).unix();
	date_to = moment( date_to, 'DD/MM/YYYY' ).unix();

	if ( date_from > date_to ) {
		setDefaultDates();
	};

});

function getDateAsTimestamp ( date ) {
	return moment( date, 'DD/MM/YYYY' ).unix();
};

function setDefaultDates () {

	$( '#date_from' ).val( moment().subtract( 7, 'days' ).format( 'DD/MM/YYYY' ) );
	$( '#date_to' ).val( moment().format( 'DD/MM/YYYY' ) );

};

function validaRut ( rut ) {

	var rexp = new RegExp(/^([0-9])+\-([kK0-9])+$/);

	if ( rut.match( rexp ) ) {

		var RUT	= rut.split( "-" );
		var elRut = RUT[0].split( '' );
		var factor = 2;
		var suma = 0;
		var dv;

		for ( var i = ( elRut.length - 1 ); i >= 0; i-- ) {
			factor = factor > 7 ? 2 : factor;
			suma += parseInt( elRut[i], 10 ) * parseInt( factor++, 10 );
		};

		dv = 11 - ( suma % 11 );
		if ( dv == 11 ) {
			dv = 0;
		} else if ( dv == 10 ) {
			dv = "k";
		};

		if ( dv == RUT[1].toLowerCase() ) {
			//console.log( "El rut es valido." );
			return true;
		} else {
		alert( "El rut es incorrecto." );
			return false;
		};
	} else {
		alert( "Formato rut incorrecto. El formato es 12345678-9" );
		return false;
	};

};

$( 'button' ).on( "mouseover", function () {
	$( this ).popover( 'show' );
});

$( 'button' ).on( "mouseout", function () {
	$( this ).popover( 'hide' );
});

$( 'div' ).on( 'mouseover', '#divPopOver', function () {
	$( this ).popover( 'show' );
});

$( 'div' ).on( 'mouseout', '#divPopOver', function () {
	$( this ).popover( 'hide' );
});

function timestamp_to_date ( date ) {
	return moment.unix( date ).format( 'DD-MM-YYYY h:mm:ss a' );
};

function drawJqueryTable ( urlSource ) {
	var table = $( '#tableCards' ).dataTable({
		"ajaxSource": urlSource,
		"destroy": true,
		"lengthChange": false,
		"ordering": false,
		"pageLength": 50,
		"paging": true,
		"processing": true,
		"scrollCollapse": true,
		"scrollX": "100%",
		"scrollY": "450px",
		"searching": false,
		"serverSide": true,
		"columns": [
			{
				'title': 'Resumen de envío',
				'render': function ( data, type, row, meta ) {
					var popBody = "<article style=\"font-size:11px;\">";
					var rowBody = " ";

					if ( row['processed_event'] ) {
						rowBody += "<span class=\"label label-default\"> </span>&nbsp;";
						popBody += "<p><span class=\"label label-default\"> </span>&nbsp;";
						popBody += " Procesado el " + timestamp_to_date( row['processed_date'] ) + "</p>";
					};
					if ( row['delivered_event'] ) {
						rowBody += "<span class=\"label label-primary\"> </span>&nbsp;";
						popBody += "<p><span class=\"label label-primary\"> </span>&nbsp;";
						popBody += " Enviado el " + timestamp_to_date( row['delivered_date'] ) + "</p>";
					};
					if ( row['opened_event'] ) {
						rowBody += "<span class=\"label label-success\"> </span>&nbsp;";
						popBody += "<p><span class=\"label label-success\"> </span>&nbsp;";
						popBody += " Leído la primera vez el  ";
						popBody += timestamp_to_date( row['opened_first_date'] ) + "<br>";
						popBody += " Leído por última vez el ";
						popBody += timestamp_to_date( row['opened_last_date'] ) + "<br>";
						popBody += " IP " + row['opened_ip'] + " " + row['opened_count'] + " veces.</p>";
					};
					if ( row['dropped_event'] ) {
						rowBody += "<span class=\"label label-warning\"> </span>&nbsp;";
						popBody += "<p><span class=\"label label-warning\"> </span>&nbsp;";
						popBody += " Rechazado el " + timestamp_to_date( row['dropped_date'] ) + "<br> ";
						popBody += " Motivo: " + (row['dropped_reason']).replace( "'", " ") + "</p>";
					};
					if ( row['bounce_event'] ) {
						rowBody += "<span class=\"label label-danger\"> </span>&nbsp;";
						popBody += "<p><span class=\"label label-danger\"> </span>&nbsp;";
						popBody += " Rebotado el " + timestamp_to_date( row['bounce_date'] ) + "<br> ";
						popBody += " Motivo: " + (row['bounce_reason']).replace( "'", " ") + "</p>";
					};
					if ( row['unsubscribe_event'] ) {
						rowBody += "<span class=\"label label-info\"> </span>&nbsp;";
						popBody += "<p><span class=\"label label-info\"> </span>&nbsp;";
						popBody += " Desuscrito el " + timestamp_to_date( row['dropped_date'] ) + "</p>";
					};
					popBody += '</article>';

					var html = "<div id=\"divPopOver\" rel=\"popover\" data-animation=\"true\" ";
					html += " data-trigger=\"hover\" data-html=\"true\" data-placement=\"right\" ";
					html += " data-container=\"body\" data-toggle=\"popover\" ";
					html += " data-content=\'" + popBody + "\'> " + rowBody + " </div>";
					return html;
				},
			},
			{
				'data': 'smtp_id',
				'title': 'Detalle',
				'render': function ( data, type, row, meta ) {
					if ( typeof( data ) === 'string' && data != null ) {
						var html = '';
						html += '<span style="font-size:16px;color:#2196f3;align:center;cursor:pointer;" title="Click para ver más detalle." class="glyphicon glyphicon-info-sign" id="spanDetail" data-smtp="' + data + '"></span>';
						return html;
					} else {
						return "";
					};
				},
			},
			{
				'data': 'adjunto1',
				'title': 'Adjuntos',
				'render': function ( data, type, row, meta ) {
					if ( data ) {
						var html = '<div style="font-size:11px;">';
						html += '<a href="' + attachUrl + data + '" title="Ver archivo adjunto" target="_blank"><span class="mdi-editor-attach-file"></span></a>';
						html += '</div>';
						return html;
					} else {
						return " ";
					};
				},
			},
			{
				'data': 'numero_folio',
				'title': 'Folio',
			},
			{
				'data': 'correo',
				'title': 'Correo',
			},
			{
				'data': 'input_date',
				'title': 'Fecha envío',
				'render': function ( data, type, row, meta ) {
					return ( !data ) ? "" : moment( data ).format( 'DD-MM-YYYY' );
				},
			},
			{
				'data': 'rut_receptor',
				'title': 'Rut receptor',
			},
			{ 
				'data': 'nombre_cliente',
				'title': 'Nombre cliente',
			},
			{ 
				'data': 'rut_emisor',
				'title': 'Rut emisor',
			},
			{ 
				'data': 'tipo_envio',
				'title': 'Tipo envío',
			},
			{ 
				'data': 'tipo_dte',
				'title': 'Tipo DTE',
			},
			{ 
				'data': 'monto',
				'title': 'Monto',
				'render': function ( data, type, row, meta ) {
					return ( !data ) ? "$0.-" : "$" + data + ".-";
				},
			},
		],
		"language": {
			"emptyTable": "No se encontraron registros.",
            "info": "Página _PAGE_ de _PAGES_",
            "infoEmpty": "No se encontraron registros.",
            "infoFiltered": "(Filtrado de _MAX_ registros).",
            "loadingRecords": "Cargando...",
            "paginate": {
            	"previous": "Anterior",
            	"next": "Siguiente",
            },
            "processing": "Proceso en curso.",
            "search": "Buscar",
            "zeroRecords": "No se encontraron registros.",
        },
	});
	table.removeClass('display');
	table.addClass('table table-hover table-striped table-condensed table-responsive');
};

/*
* Funciones para detalle de email y mostrarlos en el modal
*/
$( "#tableCards" ).on( "click", "td", function () {
	var span = $( this ).find( "#spanDetail" );
	var smtp_id = span.data( "smtp" );
	if ( smtp_id ) {
		$( '#loadingModal' ).modal( 'show', true );
		getEmailDetailAjax( smtp_id );
	};
});

function getEmailDetailAjax ( smtp_id ) {
	$.ajax({
		url: emailDetailUrl,
		type: 'GET',
		dataType: 'json',
		data: {
			'smtp_id': smtp_id,
		},
		success: function ( data ) {
			//console.log( data );
			drawEmailDetailModal( data );
		},
		error: function ( jqXHR, textStatus, errorThrown ) {
			console.log( errorThrown );
		},
	});
};

function drawEmailDetailModal ( data ) {
	var title = $( '#emailDetailTitle' );
	var body = $( '#emailDetailBody' );
	title.empty();
	body.empty();
	
	var htmlTitle = 'Detalle de ' + data.correo + " Folio Nº " + data.numero_folio;
	
	var htmlBody = '<div><br>';
	htmlBody += '<label>Empresa</label> ' + data.empresa + ' ';
	htmlBody += '<label>Rut emisor</label> ' + data.rut_emisor + ' ';
	htmlBody += '<label>Rut receptor</label> ' + data.rut_receptor + ' ';
	htmlBody += '<label>Tipo envío</label> ' + data.tipo_envio + '<br>';
	htmlBody += '<label>Folio</label> ' + data.numero_folio + ' ';
	htmlBody += '<label>Tipo doc. trib.</label> ' + data.tipo_dte + '<br>';
	htmlBody += '<label>Resolución receptor</label>';
	if ( data.resolucion_receptor ) {
		htmlBody += ' aaa' + data.resolucion_receptor + ' ';
	} else { 
		htmlBody += '---';
	};
	htmlBody += '<label>Resolución emisor</label> ';
	if ( data.resolucion_emisor ) {
		htmlBody += ' ' + data.resolucion_emisor + ' ';
	} else { 
		htmlBody += '---';
	};
	htmlBody += '<br>';
	htmlBody += '<label>Monto</label> ' + data.monto + '<br>';
	htmlBody += '<label>Fecha emisión</label> ';

	if ( data.fecha_emision ) {
		htmlBody += ' ' + timestamp_to_date( data.fecha_emision ) + ' ';
	} else { 
		htmlBody += '---';
	};
	htmlBody += '<br>';
	htmlBody += '<label>Fecha recepción</label> ';
	if ( data.fecha_recepcion ) {
		htmlBody += ' ' + timestamp_to_date( data.fecha_recepcion ) + ' ';
	} else { 
		htmlBody += '---';
	};
	htmlBody += '<br>';
	htmlBody += '<label>Estado del documento</label> ';
	if ( data.estado_documento ) {
		htmlBody += ' ' + data.estado_documento + ' ';
	} else {
		htmlBody += '---';
	};
	htmlBody += '<br>';
	htmlBody += '<label>Tipo operación</label>';
	if ( data.tipo_operacion ) {
		htmlBody += ' ' + data.tipo_operacion + ' ';
	} else {
		htmlBody += '---';
	};
	htmlBody += '<br>';
	htmlBody += '<label>Tipo receptor</label>';
	if ( data.tipo_receptor ) {
		htmlBody += ' ' + data.tipo_receptor + ' ';
	} else {
		htmlBody += '---';
	};
	htmlBody += '<br>';
	if ( data.adjunto1 ) {
		htmlBody += '<label>Adjunto</label> ';
		htmlBody += '<a href="' + attachUrl + data.adjunto1 + '" target="_blank">Ver documento adjunto</a><br>';
	};
	htmlBody += '<label>Nombre cliente</label> ' + data.nombre_cliente + '<br>';

	htmlBody += '<label>Tracking del correo:</label><br>';
	if ( data.processed_event ) {
		htmlBody += '<label class="label label-default">Procesado</label> ';
		htmlBody += 'el ' + timestamp_to_date( data.processed_date ) + '<br>'; 
	};

	if ( data.delivered_event ) {
		htmlBody += '<label class="label label-primary">Enviado</label> ';
		htmlBody += ' el ' + timestamp_to_date( data.delivered_date ) + '<br>';
	};

	if ( data.opened_event ) {
		htmlBody += '<label class="label label-success">Leído</label> ';
		htmlBody += 'primera vez el ' + timestamp_to_date( data.opened_first_date ) + ' ';
		htmlBody += 'y fue leído por ultima vez el ' + timestamp_to_date( data.opened_last_date ) + ' ';
		htmlBody += 'y ha sido leído ' + data.opened_count + ' vez/veces.<br>';
		htmlBody += 'IP lectura ' + data.opened_ip + ' Navegador web utilizado ' + data.opened_user_agent + '<br>';
	};

	if ( data.bounce_event ) {
		htmlBody +='<label class="label label-warning">Rebotado</label> ';
		htmlBody += 'el ' + timestamp_to_date( data.bounce_date ) + '<br>';
		htmlBody +='Tipo rebote ' + data.bounce_type + ' status ' + data.bounce_status + '<br>';
		htmlBody +='Razón del rebote ' + data.bounce_reason + '<br>';
	};
	

	if ( data.dropped_event ) {
		htmlBody += '<label class="label label-danger">Rechazado</label> ';
		htmlBody += 'el ' + timestamp_to_date( data.dropped_date ) + ' ';
		htmlBody += '<b>Motivo</b> ' + data.dropped_reason + '<br>';
	};

	htmlBody += '';
	htmlBody += '</div>';

	title.append( htmlTitle );
	body.append( htmlBody );

	$( '#emailDetailModal' ).modal( 'show', true );
	$( '#closeLoadingModal' ).click();
};